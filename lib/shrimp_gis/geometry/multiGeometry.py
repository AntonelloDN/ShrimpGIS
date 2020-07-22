# coding=utf-8
"""Base Geometry."""

from collections import Counter


class MultiGeometry(object):

    
    def __is_unique_type(self, geometry):
        
        types = [obj.name for obj in geometry]

        msg = "Please connect just one type among points, curves, surfaces."

        if "mesh" in types:
            raise ValueError(msg)

        if len(Counter(types)) != 1:
            raise ValueError(msg)


    def __init__(self, geometry):

        self.__is_unique_type(geometry)
        self.geometry = geometry
        self.name = "multi" + geometry[0].name

    
    def ToString(self):
        return 'ShrimpGIS::{}::{}'.format(self.name, len(self.geometry))