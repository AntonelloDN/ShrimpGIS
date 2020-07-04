# coding=utf-8
"""Rhino Curve Z for GIS."""

from curve import ShpCurve

class ShpCurveZ(ShpCurve):

    def __init__(self, geometry, number_of_division):
        ShpCurve.__init__(self, geometry, number_of_division)
        self.name = "curveZ"

    def ToString(self):
        return 'ShrimpGIS::curveZ::{}'.format(len(self.coordinates))
