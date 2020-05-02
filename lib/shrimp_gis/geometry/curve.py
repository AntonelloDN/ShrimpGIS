# coding=utf-8
"""Rhino Curve for GIS."""

from base import ShpGeometry
import Rhino


class ShpCurve(ShpGeometry):

    def __init__(self, geometry, number_of_division):
        ShpGeometry.__init__(self, geometry)
        self.name = "curve"
        self.points = self.get_points(geometry, number_of_division)

    @classmethod
    def get_points(cls, geometry, number_of_division):
        """Number of minimum points: 2"""
        if number_of_division < 2: number_of_division = 2

        if (geometry.IsPolyline()):
            geometry = geometry.ToNurbsCurve()
            points = [pt.Location for pt in geometry.Points]
        else:
            param = geometry.DivideByCount(number_of_division, True);
            points = [geometry.PointAt(t) for t in param]
            if geometry.IsClosed:
                points.append(points[0])
        return points

    def ToString(self):
        return 'ShrimpGIS::curve::{}'.format(len(self.coordinates))
