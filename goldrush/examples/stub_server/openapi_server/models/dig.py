# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Dig(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, license_id=None, pos_x=None, pos_y=None, depth=None):  # noqa: E501
        """Dig - a model defined in OpenAPI

        :param license_id: The license_id of this Dig.  # noqa: E501
        :type license_id: int
        :param pos_x: The pos_x of this Dig.  # noqa: E501
        :type pos_x: int
        :param pos_y: The pos_y of this Dig.  # noqa: E501
        :type pos_y: int
        :param depth: The depth of this Dig.  # noqa: E501
        :type depth: int
        """
        self.openapi_types = {
            'license_id': int,
            'pos_x': int,
            'pos_y': int,
            'depth': int
        }

        self.attribute_map = {
            'license_id': 'licenseID',
            'pos_x': 'posX',
            'pos_y': 'posY',
            'depth': 'depth'
        }

        self._license_id = license_id
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._depth = depth

    @classmethod
    def from_dict(cls, dikt) -> 'Dig':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The dig of this Dig.  # noqa: E501
        :rtype: Dig
        """
        return util.deserialize_model(dikt, cls)

    @property
    def license_id(self):
        """Gets the license_id of this Dig.

        ID of the license this request is attached to.  # noqa: E501

        :return: The license_id of this Dig.
        :rtype: int
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this Dig.

        ID of the license this request is attached to.  # noqa: E501

        :param license_id: The license_id of this Dig.
        :type license_id: int
        """
        if license_id is None:
            raise ValueError("Invalid value for `license_id`, must not be `None`")  # noqa: E501

        self._license_id = license_id

    @property
    def pos_x(self):
        """Gets the pos_x of this Dig.


        :return: The pos_x of this Dig.
        :rtype: int
        """
        return self._pos_x

    @pos_x.setter
    def pos_x(self, pos_x):
        """Sets the pos_x of this Dig.


        :param pos_x: The pos_x of this Dig.
        :type pos_x: int
        """
        if pos_x is None:
            raise ValueError("Invalid value for `pos_x`, must not be `None`")  # noqa: E501
        if pos_x is not None and pos_x < 0:  # noqa: E501
            raise ValueError("Invalid value for `pos_x`, must be a value greater than or equal to `0`")  # noqa: E501

        self._pos_x = pos_x

    @property
    def pos_y(self):
        """Gets the pos_y of this Dig.


        :return: The pos_y of this Dig.
        :rtype: int
        """
        return self._pos_y

    @pos_y.setter
    def pos_y(self, pos_y):
        """Sets the pos_y of this Dig.


        :param pos_y: The pos_y of this Dig.
        :type pos_y: int
        """
        if pos_y is None:
            raise ValueError("Invalid value for `pos_y`, must not be `None`")  # noqa: E501
        if pos_y is not None and pos_y < 0:  # noqa: E501
            raise ValueError("Invalid value for `pos_y`, must be a value greater than or equal to `0`")  # noqa: E501

        self._pos_y = pos_y

    @property
    def depth(self):
        """Gets the depth of this Dig.


        :return: The depth of this Dig.
        :rtype: int
        """
        return self._depth

    @depth.setter
    def depth(self, depth):
        """Sets the depth of this Dig.


        :param depth: The depth of this Dig.
        :type depth: int
        """
        if depth is None:
            raise ValueError("Invalid value for `depth`, must not be `None`")  # noqa: E501
        if depth is not None and depth > 100:  # noqa: E501
            raise ValueError("Invalid value for `depth`, must be a value less than or equal to `100`")  # noqa: E501
        if depth is not None and depth < 1:  # noqa: E501
            raise ValueError("Invalid value for `depth`, must be a value greater than or equal to `1`")  # noqa: E501

        self._depth = depth