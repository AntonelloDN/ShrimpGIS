# coding=utf-8
"""Base Geometry."""


class ShpGeometry(object):

    def __init__(self, geometry):
        self.geometry = geometry
        self.coordinates = None

    def decompose_shp_geometry(self):
        return self.coordinates
