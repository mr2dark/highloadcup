# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.wallet import Wallet  # noqa: F401,E501
from swagger_server import util


class Balance(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, balance: int=None, wallet: Wallet=None):  # noqa: E501
        """Balance - a model defined in Swagger

        :param balance: The balance of this Balance.  # noqa: E501
        :type balance: int
        :param wallet: The wallet of this Balance.  # noqa: E501
        :type wallet: Wallet
        """
        self.swagger_types = {
            'balance': int,
            'wallet': Wallet
        }

        self.attribute_map = {
            'balance': 'balance',
            'wallet': 'wallet'
        }
        self._balance = balance
        self._wallet = wallet

    @classmethod
    def from_dict(cls, dikt) -> 'Balance':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The balance of this Balance.  # noqa: E501
        :rtype: Balance
        """
        return util.deserialize_model(dikt, cls)

    @property
    def balance(self) -> int:
        """Gets the balance of this Balance.


        :return: The balance of this Balance.
        :rtype: int
        """
        return self._balance

    @balance.setter
    def balance(self, balance: int):
        """Sets the balance of this Balance.


        :param balance: The balance of this Balance.
        :type balance: int
        """
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501

        self._balance = balance

    @property
    def wallet(self) -> Wallet:
        """Gets the wallet of this Balance.


        :return: The wallet of this Balance.
        :rtype: Wallet
        """
        return self._wallet

    @wallet.setter
    def wallet(self, wallet: Wallet):
        """Sets the wallet of this Balance.


        :param wallet: The wallet of this Balance.
        :type wallet: Wallet
        """
        if wallet is None:
            raise ValueError("Invalid value for `wallet`, must not be `None`")  # noqa: E501

        self._wallet = wallet