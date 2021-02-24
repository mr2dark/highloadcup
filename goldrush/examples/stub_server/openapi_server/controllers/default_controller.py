import connexion
import six

from openapi_server.models.area import Area  # noqa: E501
from openapi_server.models.balance import Balance  # noqa: E501
from openapi_server.models.dig import Dig  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.license import License  # noqa: E501
from openapi_server.models.report import Report  # noqa: E501
from openapi_server.models.set import Set  # noqa: E501
from openapi_server import util


def cash(args):  # noqa: E501
    """cash

    Exchange provided treasure for money. # noqa: E501

    :param args: Treasure for exchange.
    :type args: str

    :rtype: Set[int]
    """
    return 'do some magic!'


def dig(args):  # noqa: E501
    """dig

    Dig at given point and depth, returns found treasures. # noqa: E501

    :param args: License, place and depth to dig.
    :type args: dict | bytes

    :rtype: List[str]
    """
    if connexion.request.is_json:
        args = Dig.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def explore_area(args):  # noqa: E501
    """explore_area

    Returns amount of treasures in the provided area at full depth. # noqa: E501

    :param args: Area to be explored.
    :type args: dict | bytes

    :rtype: Report
    """
    if connexion.request.is_json:
        args = Area.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_balance():  # noqa: E501
    """get_balance

    Returns a current balance. # noqa: E501


    :rtype: Balance
    """
    return 'do some magic!'


def health_check():  # noqa: E501
    """health_check

    Returns 200 if service works okay. # noqa: E501


    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def issue_license(args=None):  # noqa: E501
    """issue_license

    Issue a new license. # noqa: E501

    :param args: Amount of money to spend for a license. Empty array for get free license. Maximum 10 active licenses
    :type args: List[int]

    :rtype: License
    """
    return 'do some magic!'


def list_licenses():  # noqa: E501
    """list_licenses

    Returns a list of issued licenses. # noqa: E501


    :rtype: List[License]
    """
    return 'do some magic!'
