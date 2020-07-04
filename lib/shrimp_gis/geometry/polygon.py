# coding=utf-8
"""Rhino Surface for GIS."""

from curve import ShpCurve
from base import ShpGeometry
import Rhino


class ShpPolygon(ShpCurve):

    def __decompose_geometry(self, geometry):

        return Rhino.Geometry.Curve.JoinCurves(geometry.DuplicateEdgeCurves(True))

    def __init__(self, geometry, number_of_division):

        for srf in geometry.Surfaces:
            if not srf.IsPlanar():
                raise ValueError("Surfaces must be planar.")
        
        ShpGeometry.__init__(self, geometry)

        curves = self.__decompose_geometry(geometry)

        areas = [Rhino.Geometry.AreaMassProperties.Compute(crv).Area for crv in curves]
        max_area = max(areas)

        self.points = []
        for crv, area in zip(curves, areas):
            direction = crv.ClosedCurveOrientation()
            pts = ShpCurve.get_points(crv, number_of_division)

            # I suppose an hole is smaller than shape
            if (area < max_area):
                if (direction == Rhino.Geometry.CurveOrientation.Clockwise):
                    pts.reverse()
            else:
                if (direction == Rhino.Geometry.CurveOrientation.CounterClockwise):
                    pts.reverse()

            self.points.append(pts)

        self.name = "polygon"

    def ToString(self):
        return 'ShrimpGIS::polygon::{}'.format(len(self.coordinates))
