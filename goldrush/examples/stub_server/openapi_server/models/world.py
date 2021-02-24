import logging
import time
import uuid
from typing import List

import numpy as np

from openapi_server.models import Area, Dig, Report, Balance, License
import connexion.exceptions as cex
import werkzeug.exceptions as wex

MAX_LICENSES = 10

HEIGHT = 3500
WIDTH = 3500
DEPTH = 10


class WrongCoordinatesProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(422, title, detail, typ, instance, headers, ext={"code": 1000})


class WrongDepthProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(422, title, detail, typ, instance, headers, ext={"code": 1001})


class NoMoreActiveLicensesAllowedProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(409, title, detail, typ, instance, headers, ext={"code": 1002})


class TreasureIsNotDiggedProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(409, title, detail, typ, instance, headers, ext={"code": 1003})


class NoTreasureProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(404, title, detail, typ, instance, headers)


class WrongLicenseProblem(cex.ProblemException, wex.BadRequest):
    def __init__(self, title=None, detail=None, typ=None, instance=None, headers=None):
        super().__init__(403, title, detail, typ, instance, headers)


class ClientStats:
    free_licenses_issued: int = 0
    paid_licenses_issued: int = 0
    single_cell_explores_done: int = 0
    single_cell_explores_nonzero: int = 0
    digs_done: int = 0
    treasures_found: int = 0
    treasures_exchanged: int = 0
    total_found_treasure_value: int = 0
    total_exchanged_treasure_value: int = 0


def take_no_more_from(iterable, left=1000):
    for item in iterable:
        if not left:
            return
        yield item
        left -= 1


class World:
    def __init__(self, seed=0):
        self._logger = self._get_logger()

        self._seed = seed
        self._rng = np.random.default_rng(self._seed)

        self._map_size = (WIDTH, HEIGHT)
        self._depth_map = np.zeros(self._map_size)
        self._generate_treasure_map()

        self._treasure_registry = {}
        self._treasure_503_registry = set()
        self._active_licenses = {}
        self._next_free_license_after = 0.

        self._balance = 0
        self._coins = set()
        self._next_coin = 0

        self._stats = ClientStats()

    def get_world_report(self):
        with_treasure = (self._treasure_map > 0)
        total_treasures = with_treasure.sum()
        total_treasure_value = self._treasure_map.sum()
        outlines = [
            "",
            "*** WORLD REPORT ***",
            f"Configuration:\t{WIDTH} x {HEIGHT} x {DEPTH}",
            f"Total treasures:\t{int(total_treasures)}",
            f"Total treasure value:\t{int(total_treasure_value)}",
            f"Avg treasure value:\t{total_treasure_value / total_treasures :.2f}",
            f"Treasure density:\t{with_treasure.mean():.5f}",
            f"Treasure value density:\t{self._treasure_map.mean():.5f}",
            "* LAYER STATS *",
        ]
        layer_stats_titles = [
            "Layer#",
            "Tot.treas",
            "Tot.treas.val",
            "Avg.treas.val",
            "Treas.dens",
            "Treas.val.dens"
        ]
        outlines.append("\t".join(layer_stats_titles))
        col_widths = list(map(len, layer_stats_titles))
        for i in range(DEPTH):
            layer = self._treasure_map[:, :, i]
            layer_with_treasure = (layer > 0)
            outlines.append("\t".join([
                f"{i + 1:{col_widths[0]}d}",
                f"{int(layer_with_treasure.sum()):{col_widths[1]}d}",
                f"{int(layer.sum()):{col_widths[2]}d}",
                f"{layer.sum() / layer_with_treasure.sum():{col_widths[3]}.2f}",
                f"{layer_with_treasure.mean():{col_widths[4]}.5f}",
                f"{layer.mean():{col_widths[5]}.5f}",
            ]))
        return "\n".join(outlines)

    def get_client_report(self):
        outlines = [
            "*** CLIENT REPORT ***",
            f"Balance:\t{self._balance}",
            f"Licenses active:\t{len(self._active_licenses)}",
            f"Free licenses issued:\t{self._stats.free_licenses_issued}",
            f"Paid licenses issued:\t{self._stats.paid_licenses_issued}",
            f"Single cell explores done:\t{self._stats.single_cell_explores_done}",
            f"Single cell explores with treasures found:\t{self._stats.single_cell_explores_nonzero}",
            f"Single cell explore treasure found rate:\t" +
            (
                f"{self._stats.single_cell_explores_nonzero / self._stats.single_cell_explores_done:.5f}"
                if self._stats.single_cell_explores_done else "N/A"
            ),
            f"Digs done:\t{self._stats.digs_done}",
            f"Dig success rate:\t" +
            (
                f"{self._stats.treasures_found / self._stats.digs_done:.5f}"
                if self._stats.digs_done else "N/A"
            ),
            f"Treasures found:\t{self._stats.treasures_found}",
            f"Total found treasure value:\t{self._stats.total_found_treasure_value}",
            f"Treasures exchanged:\t{self._stats.treasures_exchanged}",
            f"Total exchanged treasure value:\t{self._stats.total_exchanged_treasure_value}",
            f"Treasure exchange efficiency:\t" +
            (
                f"{self._stats.treasures_exchanged / self._stats.treasures_found:.5f}"
                if self._stats.treasures_found else "N/A"
            ),
            f"Treasures not exchanged:\t{len(self._treasure_registry)}",
        ]
        return "\n".join(outlines)

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return logging.getLogger(
            "{}.{}".format(cls.__module__, cls.__qualname__)
        )

    @property
    def balance(self):
        return self._balance

    def _generate_treasure_map(self):
        densities = [489024. / WIDTH / HEIGHT / DEPTH] * DEPTH
        max_cash_size = (np.arange(DEPTH) + 1) * (DEPTH * 38.86 * 2 / 55)

        layers = []

        for depth in range(DEPTH):
            density = densities[depth]
            layer = self._rng.random(self._map_size)
            layer = np.where(layer <= density, layer, 0.) / density
            layer *= max_cash_size[depth]
            layers.append(layer.astype(np.int16))

        self._treasure_map = np.dstack(layers)

    def explore(self, area: Area):
        x_from = area.pos_x
        if not (0 <= x_from < WIDTH):
            raise WrongCoordinatesProblem()

        x_upto = x_from + area.size_x
        if not (0 < x_upto <= WIDTH):
            raise WrongCoordinatesProblem()

        y_from = area.pos_y
        if not (0 <= y_from < HEIGHT):
            raise WrongCoordinatesProblem()

        y_upto = y_from + area.size_y
        if not (0 < y_upto <= HEIGHT):
            raise WrongCoordinatesProblem()

        cube = self._treasure_map[x_from:x_upto, y_from:y_upto, :]
        with_treasure = cube > 0

        amount = int(with_treasure.sum())
        if area.size_x * area.size_y == 1:
            self._stats.single_cell_explores_done += 1
            if amount:
                self._stats.single_cell_explores_nonzero += 1
        return Report(area=area, amount=amount)

    def dig(self, dig: Dig):
        x = dig.pos_x
        if not (0 <= x < WIDTH):
            raise WrongCoordinatesProblem()
        y = dig.pos_y
        if not (0 <= y < HEIGHT):
            raise WrongCoordinatesProblem()
        depth = dig.depth
        if not (1 <= depth <= DEPTH):
            raise WrongDepthProblem()
        if depth - 1 != self._depth_map[x, y]:
            raise WrongDepthProblem()

        license_id = dig.license_id
        if license_id not in self._active_licenses:
            raise WrongLicenseProblem()

        self._stats.digs_done += 1

        self._depth_map[x, y] += 1
        value = int(self._treasure_map[x, y, depth - 1])

        license_params = self._active_licenses[license_id]
        license_params[0] += 1
        self._logger.debug("Licenses state: %s", str(self._active_licenses))
        if license_params[0] >= license_params[1]:
            del self._active_licenses[license_id]

        del license_params

        if not value:
            raise NoTreasureProblem()

        self._stats.treasures_found += 1
        self._stats.total_found_treasure_value += value

        treasure_uuid = str(uuid.uuid4())
        self._treasure_registry[treasure_uuid] = value
        draw = self._rng.random()
        if draw < 0.15:
            self._treasure_503_registry.add(treasure_uuid)
        self._treasure_map[x, y, depth - 1] = 0

        treasure_list = [treasure_uuid]

        return treasure_list

    def cash(self, treasure_uuid: str):
        if treasure_uuid not in self._treasure_registry:
            self._logger.warning("Unknown treasure: %s", treasure_uuid)
            raise TreasureIsNotDiggedProblem()

        if treasure_uuid in self._treasure_503_registry:
            self._treasure_503_registry.remove(treasure_uuid)
            raise wex.ServiceUnavailable()

        value = self._treasure_registry[treasure_uuid]
        start_coin = self._next_coin
        self._next_coin += value
        wallet_coins = list(range(start_coin, self._next_coin))
        self._coins.update(wallet_coins)

        wallet = wallet_coins

        del self._treasure_registry[treasure_uuid]
        self._balance += value
        self._stats.treasures_exchanged += 1
        self._stats.total_exchanged_treasure_value += value

        return wallet

    def get_license_list(self):
        return [
            License(id=license_id, dig_allowed=dig_allowed, dig_used=dig_used)
            for license_id, (dig_used, dig_allowed) in self._active_licenses.items()
        ]

    def report_balance(self):
        wallet_coins = list(take_no_more_from(self._coins, 1000))
        return Balance(balance=self._balance, wallet=wallet_coins)

    def _issue_new_license(self, dig_allowed):
        license_id = max(self._active_licenses.keys(), default=0) + 1

        self._active_licenses[license_id] = [0, dig_allowed]

        return License(id=license_id, dig_allowed=dig_allowed, dig_used=0)

    def issue_license(self, coins: List[int]):
        if len(self._active_licenses) >= MAX_LICENSES:
            raise NoMoreActiveLicensesAllowedProblem()

        if not coins:
            cur_time = time.time()
            if cur_time < self._next_free_license_after:
                draw = self._rng.random()
                error = wex.BadGateway() if draw < 0.7 else wex.GatewayTimeout()
                raise error

            self._next_free_license_after = cur_time + 0.05
            self._stats.free_licenses_issued += 1
            return self._issue_new_license(3)

        coin = coins[0]

        if coin not in self._coins:
            raise wex.NotFound()

        self._coins.remove(coin)
        self._balance -= 1
        self._stats.paid_licenses_issued += 1
        return self._issue_new_license(5)
