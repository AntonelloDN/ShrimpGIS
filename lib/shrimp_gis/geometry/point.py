# coding=utf-8
"""Rhino Point for GIS."""
from base import ShpGeometry

class ShpPoint(ShpGeometry):

    def __init__(self, geometry):
        ShpGeometry.__init__(self, geometry)
        self.name = "point"
        self.points = geometry

    def ToString(self):
        return 'ShrimpGIS::point::{}'.format(len(self.coordinates))
