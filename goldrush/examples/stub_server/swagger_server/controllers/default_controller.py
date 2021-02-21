from typing import Optional

import connexion
import six
import werkzeug.exceptions as wex

from swagger_server.models.treasure import Treasure
from swagger_server.models.area import Area  # noqa: E501
from swagger_server.models.balance import Balance  # noqa: E501
from swagger_server.models.dig import Dig  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.license import License  # noqa: E501
from swagger_server.models.license_list import LicenseList  # noqa: E501
from swagger_server.models.report import Report  # noqa: E501
from swagger_server.models.treasure_list import TreasureList  # noqa: E501
from swagger_server.models.wallet import Wallet  # noqa: E501
from swagger_server import util
from swagger_server.models.world import World

world: Optional[World] = None


def cash(body):  # noqa: E501
    """cash

    Exchange provided treasure for money. # noqa: E501

    :param body: Treasure for exchange.
    :type body: dict | bytes

    :rtype: Wallet
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
    return world.cash(body)


def dig(body):  # noqa: E501
    """dig

    Dig at given point and depth, returns found treasures. # noqa: E501

    :param body: License, place and depth to dig.
    :type body: dict | bytes

    :rtype: TreasureList
    """
    if connexion.request.is_json:
        body = Dig.from_dict(connexion.request.get_json())  # noqa: E501
    return world.dig(body)


def explore_area(body):  # noqa: E501
    """explore_area

    Returns amount of treasures in the provided area at full depth. # noqa: E501

    :param body: Area to be explored.
    :type body: dict | bytes

    :rtype: Report
    """
    if connexion.request.is_json:
        body = Area.from_dict(connexion.request.get_json())  # noqa: E501
    return world.explore(body)


def get_balance():  # noqa: E501
    """get_balance

    Returns a current balance. # noqa: E501


    :rtype: Balance
    """
    return world.report_balance()


def health_check():  # noqa: E501
    """health_check

    Returns 200 if service works okay. # noqa: E501


    :rtype: Dict[str, object]
    """
    if not world:
        raise wex.ServiceUnavailable()
    return 'do some magic!'


def issue_license(body=None):  # noqa: E501
    """issue_license

    Issue a new license. # noqa: E501

    :param body: Amount of money to spend for a license. Empty array for get free license. Maximum 10 active licenses
    :type body: List[]

    :rtype: License
    """
    return world.issue_license(body)


def list_licenses():  # noqa: E501
    """list_licenses

    Returns a list of issued licenses. # noqa: E501


    :rtype: LicenseList
    """
    return world.get_license_list()
