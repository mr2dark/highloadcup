# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.area import Area
from openapi_server import util

from openapi_server.models.area import Area  # noqa: E501

class Report(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, area=None, amount=None):  # noqa: E501
        """Report - a model defined in OpenAPI

        :param area: The area of this Report.  # noqa: E501
        :type area: Area
        :param amount: The amount of this Report.  # noqa: E501
        :type amount: int
        """
        self.openapi_types = {
            'area': Area,
            'amount': int
        }

        self.attribute_map = {
            'area': 'area',
            'amount': 'amount'
        }

        self._area = area
        self._amount = amount

    @classmethod
    def from_dict(cls, dikt) -> 'Report':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The report of this Report.  # noqa: E501
        :rtype: Report
        """
        return util.deserialize_model(dikt, cls)

    @property
    def area(self):
        """Gets the area of this Report.


        :return: The area of this Report.
        :rtype: Area
        """
        return self._area

    @area.setter
    def area(self, area):
        """Sets the area of this Report.


        :param area: The area of this Report.
        :type area: Area
        """
        if area is None:
            raise ValueError("Invalid value for `area`, must not be `None`")  # noqa: E501

        self._area = area

    @property
    def amount(self):
        """Gets the amount of this Report.

        Non-negative amount of treasures/etc.  # noqa: E501

        :return: The amount of this Report.
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this Report.

        Non-negative amount of treasures/etc.  # noqa: E501

        :param amount: The amount of this Report.
        :type amount: int
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501
        if amount is not None and amount < 0:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `0`")  # noqa: E501

        self._amount = amount