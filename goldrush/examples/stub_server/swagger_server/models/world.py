import logging
import time
import uuid
from typing import List

import numpy as np

from swagger_server.models import Area, Dig, TreasureList, Report, Amount, Wallet, Balance, LicenseList, \
    License
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
        self._active_licenses = {}
        self._next_free_license_after = 0.

        self._balance = 0
        self._coins = set()
        self._next_coin = 0

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return logging.getLogger(
            "{}.{}".format(cls.__module__, cls.__qualname__)
        )

    @property
    def balance(self):
        return self._balance

    def _generate_treasure_map(self):
        densities = (np.arange(10) + 1) * 0.01
        max_cash_size = (np.arange(10) + 1) * 10

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
        return Report(area=area, amount=Amount.from_dict(amount))

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
            raise wex.NotFound()

        self._depth_map[x, y] += 1
        value = int(self._treasure_map[x, y, depth - 1])

        self._active_licenses[license_id] -= 1
        self._logger.debug("Licenses state: %s", str(self._active_licenses))
        if self._active_licenses[license_id] <= 0:
            del self._active_licenses[license_id]

        if not value:
            raise NoTreasureProblem()

        treasure_uuid = str(uuid.uuid4())
        self._treasure_registry[treasure_uuid] = value
        self._treasure_map[x, y, depth - 1] = 0

        treasure_list = TreasureList.from_dict([treasure_uuid])

        return treasure_list

    def cash(self, treasure_uuid: str):
        if treasure_uuid not in self._treasure_registry:
            self._logger.warning("Unknown treasure: %s", treasure_uuid)
            raise TreasureIsNotDiggedProblem()

        value = self._treasure_registry[treasure_uuid]
        start_coin = self._next_coin
        self._next_coin += value
        wallet_coins = list(range(start_coin, self._next_coin))
        self._coins.update(wallet_coins)

        wallet = Wallet.from_dict(wallet_coins)

        del self._treasure_registry[treasure_uuid]
        self._balance += value

        return wallet

    def get_license_list(self):
        return LicenseList.from_dict(list(self._active_licenses.keys()))

    def report_balance(self):
        wallet_coins = list(take_no_more_from(self._coins, 1000))
        wallet = Wallet.from_dict(wallet_coins)
        return Balance(balance=self._balance, wallet=wallet)

    def _issue_new_license(self, dig_allowed):
        license_id = max(self._active_licenses.keys(), default=0) + 1

        self._active_licenses[license_id] = dig_allowed

        return License(id=license_id, dig_allowed=Amount.from_dict(dig_allowed), dig_used=Amount.from_dict(0))

    def issue_license(self, coins: List[int]):
        if len(self._active_licenses) >= MAX_LICENSES:
            raise NoMoreActiveLicensesAllowedProblem()

        if not coins:
            cur_time = time.time()
            if cur_time < self._next_free_license_after:
                raise wex.NotFound()

            self._next_free_license_after = cur_time + 0.1
            return self._issue_new_license(3)

        coin = coins[0]

        if coin not in self._coins:
            raise wex.NotFound()

        self._coins.remove(coin)
        self._balance -= 1
        return self._issue_new_license(5)
