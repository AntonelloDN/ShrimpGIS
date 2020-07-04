# coding=utf-8
"""Rhino Surface Z for GIS."""

from polygon import ShpPolygon

class ShpPolygonZ(ShpPolygon):

    def __init__(self, geometry, number_of_division):
        ShpPolygon.__init__(self, geometry, number_of_division)

        self.name = "polygonZ"

    def ToString(self):
        return 'ShrimpGIS::polygonZ::{}'.format(len(self.coordinates))
