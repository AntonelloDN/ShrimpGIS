# coding=utf-8
"""Shape field. Gismo tag to export."""
import Rhino


class Location(object):
    """This class create Envimet Location Attributes (Location Name, Latitude, Longitude)."""

    def __init__(self, name = "ShrimpGIS-Location", latitude = 0, longitude = 0, anchor_point = Rhino.Geometry.Point3d.Origin):
        self.name = name
        self.__latitude = latitude
        self.__longitude = longitude
        self.anchor_point = anchor_point

    @property
    def latitude(self):
        """Latitude limits (-80.0 to 84.0) """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = 0
        if (value <= 84 and value >= -80):
            self.__latitude = value

    @property
    def longitude(self):
        """Latitude limits (-180.0 to 180.0) """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        self.__longitude = 0
        if (value <= 180 and value >= -180):
            self.__longitude = value

    def ToString(self):
        return "{0}::{1}::{2}".format(self.name, self.__latitude, self.__longitude)
