# coding=utf-8
"""Rhino Point Z for GIS."""

from point import ShpPoint

class ShpPointZ(ShpPoint):

    def __init__(self, geometry):
        ShpPoint.__init__(self, geometry)
        self.name = "pointZ"

    def ToString(self):
        return 'ShrimpGIS::pointZ::{}'.format(len(self.coordinates))
