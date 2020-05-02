# coding=utf-8
"""Rhino Mesh for GIS."""

from base import ShpGeometry
import Rhino


class ShpMesh(ShpGeometry):

    def __init__(self, geometry):
        ShpGeometry.__init__(self, geometry)
        faces = geometry.Faces
        faces.ConvertQuadsToTriangles()
        self.name = "mesh"

        vertices = self.__get_vertices(geometry)
        self.points = vertices

    def __get_vertices(self, geometry):
        vertices = []
        for f in geometry.Faces:

            v_a = geometry.Vertices[f.A]
            v_b = geometry.Vertices[f.B]
            v_c = geometry.Vertices[f.C]

            a_pt = [v_a.X, v_a.Y, v_a.Z]
            b_pt = [v_b.X, v_b.Y, v_b.Z]
            c_pt = [v_c.X, v_c.Y, v_c.Z]

            vertices.append([a_pt, b_pt, c_pt])

        return vertices

    def ToString(self):
        return 'ShrimpGIS::mesh::{}'.format(len(self.coordinates))
