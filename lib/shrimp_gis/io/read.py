# coding=utf-8
"""Shpfile reader. It reads shapefile (support for ESRI Shapefiles WGS84 only)."""

from shapefile import TRIANGLE_STRIP
import shapefile
from collections import deque
import Grasshopper
import Rhino
import System
import os
from ..field import Field


class ShpReader(object):

    tol = 0.01

    __supportLevel = {
            "supported": (1, 3, 5),
            "supported with z" : (11, 13, 15),
            "not supported" : (8, 18, 21, 23, 25, 28, 31)
            }

    __rhinoType = {
            "point": (1, 11),
            "curve": (3, 13),
            "surface": (5, 15)
            }


    def is_shp_file_wgs84(self, file):
        """
        Temp method: This Method check if prj file is WGS84.
        """
        path = os.path.splitext(file)[0] + ".prj"
        try:
            with open(path, 'r') as prj:
                content = prj.read()
                # ESRI WKT or OGC WKT
                if (not "GCS_WGS_1984" in content):
                    return False
                return True
        except OSError as e:
            return False


    def __get_key_value_for_status(self, type, property):

        message = None # for not supported
        for i, values in enumerate(property.values()):
            if type in values:
                message = property.keys()[i]

        return message


    def __get_num_of_geometry(self, sf_reader_instance):

        return len(sf_reader_instance.shapes())


    def __create_fields(self, sf_reader_instance):
        """
        Private method to create Shp Fields from shp file
        """
        def get_field_values(sf_reader_instance):

            values = []
            for i in range(self.__get_num_of_geometry(sf_reader_instance)):
                values.append(sf_reader_instance.record(i))

            return map(list, zip(*values))

        def get_field_name(sf_reader_instance):

            return map(list, zip(*sf_reader_instance.fields[1:]))[0]

        field_names = get_field_name(sf_reader_instance)
        field_values = get_field_values(sf_reader_instance)

        # all as char. You can parse them easily with GH
        return [Field(vl, fn, type=1, length=0, decimal=0) for fn, vl in zip(field_names, field_values)]


    def __get_geometry_coordinates(self, sf_reader_instance):

        points = []
        for i in range(self.__get_num_of_geometry(sf_reader_instance)):
            pts = sf_reader_instance.shape(i).points
            points.append(pts)

        return points


    def __get_parts(self, sf_reader_instance):

        parts = []
        for i in range(self.__get_num_of_geometry(sf_reader_instance)):
            part = sf_reader_instance.shape(i).parts
            parts.append(part)

        return parts


    def __get_z_values(self, sf_reader_instance):

        z_val = []
        for i in range(self.__get_num_of_geometry(sf_reader_instance)):
            z = sf_reader_instance.shape(i).z
            z_val.append(z)

        return z_val


    def adjust_rh_points(self, gh_pts):

        nested_point = []
        for geop, pts in zip(self.parts, gh_pts):
            nested_point.append(self.split_list_by_index_list(pts, geop))

        return nested_point


    @staticmethod
    def split_list_by_index_list(collection, index_list):

        items = deque(index_list)
        items.rotate(-1)
        shiftedList = list(items)[:-1]
        splitter = map(lambda a, b : [a, b], index_list, shiftedList)
        return map(lambda x : collection[x[0]:x[1]], splitter)


    def create_rh_curve(self, gh_pts):

        cullValue = []
        curves = []

        for i, pts in enumerate(gh_pts):
            curves.append(Rhino.Geometry.PolylineCurve(pts))

        return curves


    def surface_post_processing(self, adjusted_points):

        geometries = Grasshopper.DataTree[System.Object]()

        def create_surface_from_curve(curves):
            return Rhino.Geometry.Brep.CreatePlanarBreps(curves, self.tol)

        missing_geometry = []

        gh_nested_curve = [self.create_rh_curve(geo) for geo in adjusted_points]

        for i, curves in enumerate(gh_nested_curve):

            path = Grasshopper.Kernel.Data.GH_Path(i)
            surf = create_surface_from_curve(curves)
            if surf == None:
                missing_geometry.append(i)
            else:
                geometries.AddRange(surf, path)

        return geometries, missing_geometry


    def curve_post_processing(self, adjusted_points):

        geometries = Grasshopper.DataTree[System.Object]()

        missing_geometry = []

        gh_nested_curve = [self.create_rh_curve(geo) for geo in adjusted_points]

        for i, curves in enumerate(gh_nested_curve):

            path = Grasshopper.Kernel.Data.GH_Path(i)
            if (not curves):
                missing_geometry.append(i)
            else:
                geometries.AddRange(curves, path)

        return geometries, missing_geometry


    def point_post_processing(self, adjusted_points):

        geometries = Grasshopper.DataTree[System.Object]()

        missing_geometry = []

        for i, points in enumerate(adjusted_points):

            path = Grasshopper.Kernel.Data.GH_Path(i)
            if (not points):
                missing_geometry.append(i)
            else:
                geometries.AddRange(points[0], path)

        return geometries, missing_geometry


    def read_shp_file(self, file):

        sf = shapefile.Reader(file)
        self.type = sf.shapeType
        self.type_name = sf.shapeTypeName

        self.level = self.__get_key_value_for_status(self.type, self.__supportLevel)
        self.rhType = self.__get_key_value_for_status(self.type, self.__rhinoType)

        if (self.level == "supported" or self.level == "supported with z"):
            self.fields = self.__create_fields(sf)
            self.points = self.__get_geometry_coordinates(sf)
            self.parts = self.__get_parts(sf)

            # create parts if shp is type 'point'
            if (self.type in self.__rhinoType["point"]):
                if(not reduce(sum, self.parts)):
                    self.parts = [[0]]*len(self.parts)

        # flat list of Z-values
        if self.level == "supported with z":
            self.z = self.__get_z_values(sf)


    def post_processing(self, gh_pts, file):

        geometries, missing_geometry = None, None

        if (self.points and self.parts):
            
            gh_part_points = self.adjust_rh_points(gh_pts)

            if (self.type in self.__rhinoType["point"]):
                geometries, missing_geometry = self.point_post_processing(gh_part_points)

            elif (self.type in self.__rhinoType["curve"]):
                geometries, missing_geometry = self.curve_post_processing(gh_part_points)

            elif (self.type in self.__rhinoType["surface"]):
                geometries, missing_geometry = self.surface_post_processing(gh_part_points)


            return geometries, missing_geometry

    @classmethod
    def decompose_fields(cls, fields):

        value_tree = Grasshopper.DataTree[System.Object]()
        names = []

        for i, field in enumerate(fields):
            names.append(field.name)
            values = field.values
            path = Grasshopper.Kernel.Data.GH_Path(i)
            value_tree.AddRange(values, path)

        return value_tree, names
