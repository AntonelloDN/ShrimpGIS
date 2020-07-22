# coding=utf-8
"""Shpfile reader. It reads shapefile (support for ESRI Shapefiles WGS84 only)."""

from shapefile import TRIANGLE_STRIP
import shapefile
import pygeoj
from collections import deque
import Grasshopper
import Rhino
import System
import os
from ..field import Field
from .transformation import from_lat_lon_to_utm


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

    def __init__(self, file):

        self.file_name = file

        if (self.__is_shp_file_wgs84()):

            self.sf = shapefile.Reader(file)
            self.__set_shape_attributes()


    def __is_shp_file_wgs84(self):
        """
            Temp method: This Method check if prj file is WGS84.
        """
        msg = "Only WGS84 (EPSG:4326) is supported.\nPlease reproject vectors using a GIS software (e.g. QGIS) before importing it."
        path = os.path.splitext(self.file_name)[0] + ".prj"

        try:
            with open(path, 'r') as prj:
                content = prj.read()
                # ESRI WKT or OGC WKT
                if (not "GCS_WGS_1984" in content):
                    raise ValueError(msg)
                return True
        except OSError as e:
            raise ValueError(msg)


    def __get_key_value_for_status(self, type, property):

        message = None # for not supported
        for i, values in enumerate(property.values()):
            if type in values:
                message = property.keys()[i]

        return message


    def __get_num_of_geometry(self):
        """
            Get SHP Length
        """
        return len(self.sf.shapes())


    def __create_fields(self):
        """
            Get SHP Fields from shp file
        """
        def get_field_values():

            values = []
            for i in range(self.__get_num_of_geometry()):
                values.append(self.sf.record(i))

            return map(list, zip(*values))

        def get_field_name():

            return map(list, zip(*self.sf.fields[1:]))[0]

        field_names = get_field_name()
        field_values = get_field_values()

        # all as char. You can parse them easily with GH
        return [Field(vl, fn, type=1, length=0, decimal=0) for fn, vl in zip(field_names, field_values)]


    def __get_geometry_coordinates(self):
        """
            Get SHP Coordinates from file
        """
        points = []
        for i in range(self.__get_num_of_geometry()):
            pts = self.sf.shape(i).points
            points.append(pts)

        return points


    def __get_parts(self):
        """
            Get SHP Parts from file
        """
        parts = []
        for i in range(self.__get_num_of_geometry()):
            part = self.sf.shape(i).parts
            parts.append(part)

        return parts


    def __get_z_values(self):
        """
            Get SHP Z from file
        """
        z_val = []
        for i in range(self.__get_num_of_geometry()):
            z = self.sf.shape(i).z
            z_val.append(z)

        return z_val


    def __adjust_rh_points(self, gh_pts):

        nested_point = []
        for geop, pts in zip(self.parts, gh_pts):
            nested_point.append(self.split_list_by_index_list(pts, geop))

        return nested_point
    

    def __set_shape_attributes(self):
        """
            Set Rhino SHP attributes
        """
        self.type = self.sf.shapeType
        self.type_name = self.sf.shapeTypeName

        self.level = self.__get_key_value_for_status(self.type, self.__supportLevel)
        self.rhType = self.__get_key_value_for_status(self.type, self.__rhinoType)

        if (self.level == "supported" or self.level == "supported with z"):
            self.fields = self.__create_fields()
            self.points = self.__get_geometry_coordinates()
            self.parts = self.__get_parts()

            # create parts if shp is type 'point'
            if (self.type in self.__rhinoType["point"]):
                if(not reduce(sum, self.parts)):
                    self.parts = [[0]]*len(self.parts)

        # flat list of Z-values
        if self.level == "supported with z":
            self.z = self.__get_z_values()
    

    @staticmethod
    def split_list_by_index_list(collection, index_list):

        items = deque(index_list)
        items.rotate(-1)
        shiftedList = list(items)[:-1]
        splitter = map(lambda a, b : [a, b], index_list, shiftedList)
        return map(lambda x : collection[x[0]:x[1]], splitter)


    def create_rh_curve(self, gh_pts):

        curves = []

        for pts in gh_pts:
            curves.append(Rhino.Geometry.PolylineCurve(pts))

        return curves


    def __surface_post_processing(self, adjusted_points):

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


    def __curve_post_processing(self, adjusted_points):

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


    def __point_post_processing(self, adjusted_points):

        geometries = Grasshopper.DataTree[System.Object]()

        missing_geometry = []

        for i, points in enumerate(adjusted_points):

            path = Grasshopper.Kernel.Data.GH_Path(i)
            if (not points):
                missing_geometry.append(i)
            else:
                geometries.AddRange(points[0], path)

        return geometries, missing_geometry


    def get_georeferenced_rhino_geometry(self, gh_pts):

        geometries, missing_geometry = None, None

        if (self.points and self.parts):
            
            gh_part_points = self.__adjust_rh_points(gh_pts)

            if (self.type in self.__rhinoType["point"]):
                geometries, missing_geometry = self.__point_post_processing(gh_part_points)

            elif (self.type in self.__rhinoType["curve"]):
                geometries, missing_geometry = self.__curve_post_processing(gh_part_points)

            elif (self.type in self.__rhinoType["surface"]):
                geometries, missing_geometry = self.__surface_post_processing(gh_part_points)


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



class GeojsonReader(ShpReader):

    def __init__(self, file):

        self.file = pygeoj.load(file)
        self.fields = self.__create_fields()
        self.type = self.get_all_type()
        self.coordinates = self.get_all_coordinates()

    
    def get_all_field_name(self):
        """
            Get the list of geojson properties
        """
        keys = []
        for feature in self.file:
            keys.extend(feature.properties.keys())
        
        return list(dict.fromkeys(keys))


    def get_all_type(self):
        """
            Get the list of geojson type
        """
        return [feature.geometry.type for feature in self.file]


    def get_all_coordinates(self):
        """
            Get the list of geojson coordinates
        """
        return [feature.geometry.coordinates for feature in self.file]


    def __create_fields(self):
        """
            Create Shp Fields from GeoJson file
        """
        fields = [Field([], fn, type=1, length=0, decimal=0) for fn in self.get_all_field_name()]
        
        for i, feature in enumerate(self.file):
            
            path = Grasshopper.Kernel.Data.GH_Path(i)
            
            for field in fields:
                if field.name in feature.properties.keys():

                    content = feature.properties[field.name]

                    if type(content) == dict:
                        content = str(content)

                    field.values.append(content)
                else:
                    field.values.append(None)

        # all as char. You can parse them easily with GH
        return fields


    def __multi_surface_post_processing(self, points):
        """
            Create Surface from MultiPolygon
        """
        geometries = []
        for pts in points:
            geometries.extend(self.__surface_post_processing(pts))
        
        return geometries


    def __surface_post_processing(self, points):
        """
            Create Surface from Polygon and Polygon with holes
        """
        def create_surface_from_curve(curves):
            return Rhino.Geometry.Brep.CreatePlanarBreps(curves, ShpReader.tol)
        
        curves = self.create_rh_curve(points)
        surfaces = create_surface_from_curve(curves)
        
        return surfaces


    def __curve_post_processing(self, points):
        """
            Create Curves
        """
        return self.create_rh_curve(points)


    def __get_point_from_geopoint(self, points, location):
        """
            Get Rhino point from geojson Point
        """
        points = from_lat_lon_to_utm(points, location)

        rh_points = []
        for pt in points:
            rh_points.append(Rhino.Geometry.Point3d(pt[0], pt[1], 0))
        return rh_points


    def __get_point_from_poly_or_multistring(self, geometry, location):
        """
            Get Rhino point from geojson Polygon or Multistring
        """
        rh_points = []
        for geo in geometry:
            rh_points.append(self.__get_point_from_geopoint(geo, location))
        
        return rh_points


    def __get_point_from_multipoly(self, geometry, location):
        """
            Get Rhino point from geojson Multipolygon
        """
        rh_points = []
        for geo in geometry:
            rh_points.append(self.__get_point_from_poly_or_multistring(geo, location))
        
        return rh_points


    def get_georeferenced_rhino_geometry(self, location):
        """
            Get Georeferenced Rhino Geometries a in Data Tree
        """
        #TODO: Implement a method for missing geometries, if necessary.
        geo_list = []

        location.set_utm()

        for geo_type, geo in zip(self.type, self.coordinates):
            if geo_type == "Polygon":
                pts = self.__get_point_from_poly_or_multistring(geo, location)
                geo_list.append(self.__surface_post_processing(pts))
            elif geo_type == "MultiPolygon":
                pts = self.__get_point_from_multipoly(geo, location)
                geo_list.append(self.__multi_surface_post_processing(pts))
            elif geo_type == "LineString":
                pts = self.__get_point_from_geopoint(geo, location)
                geo_list.append(self.create_rh_curve([pts]))
            elif geo_type == "MultiLineString":
                pts = self.__get_point_from_poly_or_multistring(geo, location)
                geo_list.append(self.create_rh_curve(pts))
            elif geo_type == "Point":
                pts = self.__get_point_from_geopoint([geo], location)
                geo_list.append(pts)
            elif geo_type == "MultiPoint":
                pts = self.__get_point_from_geopoint(geo, location)
                geo_list.append(pts)

        geometries = Grasshopper.DataTree[System.Object]()

        for i, geo in enumerate(geo_list):
            path = Grasshopper.Kernel.Data.GH_Path(i)
            geometries.AddRange(geo, path)

        return geometries
    
