# coding=utf-8
"""
Shpfile writer. It writes shapefile (support for ESRI Shapefiles WGS84 only).
Raster writer. It writes asc files and UTM WGS84 prj files.
"""

from shapefile import TRIANGLE_STRIP
import shapefile
import pygeoj
import Grasshopper
import os
import uuid
from ..field import Field


class AscWriter(object):

    def __init__(self, matrix, pixel_size, xllcenter, yllcenter):

        self.ERSI_ASCII = {
            "ncols": matrix.num_x,
            "nrows": matrix.num_y,
            "xllcenter": xllcenter,
            "yllcenter": yllcenter,
            "cellsize": pixel_size,
            "NODATA_value" : -9999
        }

        self.matrix = matrix.ASCII_matrix
    
    def get_asc(self, folder, name, prj_text):

        full_path_asc = os.path.join(folder, name + ".asc")
        full_path_prj = os.path.join(folder, name + ".prj")

        with open(full_path_asc, 'w') as f:
            
            header = []
            for k, v in self.ERSI_ASCII.items():
                header.append(" ".join(map(str, [k, v])))
            header = "\n".join(header)
            
            f.writelines(header)
            f.writelines("\n")
            f.writelines(self.matrix)
        
        with open(full_path_prj, 'w') as f:
            f.write(prj_text)
        
        return full_path_asc


class ShpWriter(object):

    def __is_unique_type(self, shp_geometry):

        main_type = shp_geometry[0].name
        for geo in shp_geometry:
            if geo.name != main_type:
                return False, main_type
        return True, main_type


    def field_legth_checking(self, shp_field, shp_geometry):

        for field in shp_field:
            if len(field.values) != len(shp_geometry):
                return False
        return True


    def create_valid_folder(self, folder):
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except:
                return False
        return True


    def __write_curve(self, shp_geometry, shp_write):
        [shp_write.line([[[pt[1], pt[0]] for pt in geo.coordinates]]) for geo in shp_geometry]


    def __write_curvez(self, shp_geometry, shp_write):
        [shp_write.linez([[[pt[1], pt[0], pt[2]] for pt in geo.coordinates]]) for geo in shp_geometry]


    def __write_polygon(self, shp_geometry, shp_write):
        for geo in shp_geometry:
            chunk = []
            for pts in geo.coordinates:
                chunk.append([[pt[1], pt[0]] for pt in pts])
            shp_write.poly(chunk)


    def __write_polygonz(self, shp_geometry, shp_write):
        for geo in shp_geometry:
            chunk = []
            for pts in geo.coordinates:
                chunk.append([[pt[1], pt[0], pt[2]] for pt in pts])
            shp_write.polyz(chunk)


    def __write_point(self, shp_geometry, shp_write):
        for geo in shp_geometry:
            for pt in geo.coordinates:
                shp_write.point(pt[1], pt[0])


    def __write_pointz(self, shp_geometry, shp_write):
        for geo in shp_geometry:
            for pt in geo.coordinates:
                shp_write.pointz(pt[1], pt[0], pt[2])


    def __write_multy_patch(self, shp_geometry, shp_write):
        for geo in shp_geometry:
            parts = []
            for face_points, face_coordinates in zip(geo.points, geo.coordinates):
                face = []
                for pt, cd in zip(face_points, face_coordinates):
                    face.append([cd[1], cd[0], pt[2]])
                parts.append(face)
            shp_write.multipatch(parts,partTypes=[TRIANGLE_STRIP]*len(parts))


    #TODO: Add epsg code as input. Call epsg.io API or other to retrieve prj string. Write prj file. It does not work within Rhino for now.
    def write_prj_file(self, folder, file_name):
        wgs84prjString = "GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433]]"

        with open(os.path.join(folder, file_name + ".prj"), "w") as prj_file:
            prj_file.write(wgs84prjString)


    def write_shp_file(self, folder, file_name, shp_geometry, shp_field):

        if (len(shp_field) == 0):
            values = [uuid.uuid4() for i in range(len(shp_geometry))]
            shp_field = [Field(values, 'UUID', 'C', 40, 0)]

        unique_test, main_type = self.__is_unique_type(shp_geometry)

        if (unique_test and self.field_legth_checking(shp_field, shp_geometry) and self.create_valid_folder(folder)):

            full_path = os.path.join(folder, file_name + ".shp")
            w = shapefile.Writer(os.path.join(folder, file_name + ".shp"))

            values = []
            for field in shp_field:
                if field.type == 'L':
                    values.append(map(int, field.values))
                    continue
                values.append(field.values)

            if (main_type == "curve"):
                self.__write_curve(shp_geometry, w)

            elif (main_type == "polygon"):
                self.__write_polygon(shp_geometry, w)

            elif (main_type == "point"):
                self.__write_point(shp_geometry, w)

            elif (main_type == "mesh"):
                self.__write_multy_patch(shp_geometry, w)

            elif (main_type == "curveZ"):
                self.__write_curvez(shp_geometry, w)

            elif (main_type == "polygonZ"):
                self.__write_polygonz(shp_geometry, w)

            elif (main_type == "pointZ"):
                self.__write_pointz(shp_geometry, w)

            # unwrap fields
            for field in shp_field:
                w.field(field.name, field.type, field.length, field.decimal)

            for val in map(list, zip(*values)):
                w.record(*val)

            # ESRI WKT
            self.write_prj_file(folder, file_name)

            w.close()

            return full_path

        else:
            return False


class GeojsonWriter(ShpWriter):

    #TODO: Implement z values. Only 2d for now.
    def __write_point(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"Point"}

        geom["coordinates"] = [shp_geometry.coordinates[0][1], shp_geometry.coordinates[0][0]]

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )


    def __write_multi_point(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"MultiPoint"}

        coordinates = []
        for geo in shp_geometry.geometry:
            for pt in geo.coordinates:
                coordinates.append([pt[1], pt[0]])
        
        geom["coordinates"] = coordinates

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )
    

    def __write_linestring(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"LineString"}

        geom["coordinates"] = [[pt[1], pt[0]] for pt in shp_geometry.coordinates]

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )
    

    def __write_multi_linestring(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"MultiLineString"}

        coordinates = []
        for geo in shp_geometry.geometry:
            coordinates.append([[pt[1], pt[0]] for pt in geo.coordinates])

        geom["coordinates"] = coordinates

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )


    def __write_polygon(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"Polygon"}

        coordinates = []
        for geo in shp_geometry.coordinates:
            coordinates.append([[pt[1], pt[0]] for pt in geo])
        
        geom["coordinates"] = coordinates

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )
    
    
    def __write_multi_polygon(self, index, geojson, shp_geometry, shp_field):

        prop = {}
        geom = {"type":"MultiPolygon"}

        coordinates = []
        for geo in shp_geometry.geometry:
            curve = []
            for pts in geo.coordinates:
                curve.append([[pt[1], pt[0]] for pt in pts])
            coordinates.append(curve)
        
        geom["coordinates"] = coordinates

        for field in shp_field:
            prop[field.name] = field.values[index]
        
        geojson.add_feature ( properties=prop, geometry=geom )
    

    def write_geojson_file(self, folder, file_name, shp_geometry, shp_field):

        if (len(shp_field) == 0):
            values = [str(uuid.uuid4()) for i in range(len(shp_geometry))]
            shp_field = [Field(values, 'UUID', 'C', 40, 0)]

        full_path = os.path.join(folder, file_name + ".json")

        geojson = pygeoj.new()

        if (self.field_legth_checking(shp_field, shp_geometry) and self.create_valid_folder(folder)):

            for i, geometry in enumerate(shp_geometry):
                if geometry.name == "point":
                    self.__write_point(i, geojson, geometry, shp_field)
                elif geometry.name == "multipoint":
                    self.__write_multi_point(i, geojson, geometry, shp_field)
                elif geometry.name == "curve":
                    self.__write_linestring(i, geojson, geometry, shp_field)
                elif geometry.name == "multicurve":
                    self.__write_multi_linestring(i, geojson, geometry, shp_field)
                elif geometry.name == "polygon":
                    self.__write_polygon(i, geojson, geometry, shp_field)
                elif geometry.name == "multipolygon":
                    self.__write_multi_polygon(i, geojson, geometry, shp_field)
                
            geojson.add_all_bboxes()
            geojson.update_bbox()
            geojson.save(full_path)

            return full_path
        
        else:
            return False
    
    @classmethod
    def merge_geojson(cls, folder, file_name, files):

        geojson = pygeoj.new()
        for path in files:
            f = pygeoj.load(path)
            for feature in f:
                geojson.add_feature(obj=feature)

        full_path = os.path.join(folder, file_name + ".json")

        geojson.add_all_bboxes()
        geojson.update_bbox()
        geojson.save(full_path)

        return full_path


        