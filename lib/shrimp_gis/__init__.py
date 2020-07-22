#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ShrimpGIS - Basic Grasshopper plugin to read and write shapefile.
It uses: utm 0.5.0; pyshp 2.1.0; pygeoj 1.0.0
"""

# modules
import geometry
import io
import utm
from field import Field
from location import Location

__author__ = 'antonellodinunzio@gmail.com'
__copyright__ = 'Antonello Di Nunzio'
__credits__ = 'Antonello Di Nunzio'
__license__ = 'GNU GPL V.3+'
__version__ = '1.0.3'
__maintainer__ = 'Antonello Di Nunzio'
__email__ = 'plugin@antonellodinunzio.com'
__status__ = 'release'
