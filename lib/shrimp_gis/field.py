# coding=utf-8
"""Shape field."""


class Field(object):

    types = {0: 'C', 1: 'N', 2: 'F', 3: 'L', 4: 'D', 5: 'M'}

    def __init__(self, values, name ='TAG', type = 'C', length = 40, decimal = 0):
        self.__name = name
        self.values = values
        self.type = type
        self.length = length
        self.decimal = decimal

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        """ 10 char limit """
        self.__name = value
        if (len(value) > 10):
            self.__name = value[:10]

    @classmethod
    def get_type(cls, index):
        return cls.types[index]

    def ToString(self):
        return 'ShrimpGIS::field::{}'.format(self.name)
