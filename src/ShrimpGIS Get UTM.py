# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Get UTM information from Shrimp point.
-
The UTM (Universal Transverse Mercator) system divides the surface of the earth up into a grid. Each grid is identified by a number, a zone number and a letter.
    Args:
        _shp_point: Shrimp point.
    
    Returns:
        utm_easting: Easting value of UTM coordinate.
        utm_northing: Northing value of UTM coordinate.
        zone_number: UTM zone number.
        -
        The UTM system divides the Earth into 60 zones, each 6° of longitude in width. Zone 1 covers longitude 180° to 174° W.
        zone_letter: UTM zone letter.
"""

ghenv.Component.Name = "ShrimpGIS Get UTM"
ghenv.Component.NickName = "shrimp_get_utm"
ghenv.Component.Message = "1.0.0"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "2 || Utils"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import os
import sys
##################ShrimpGIS#####################
try:
    user_path = os.getenv("APPDATA")
    sys.path.append(user_path)
    from shrimp_gis import __version__
    from shrimp_gis import Location
    from shrimp_gis.geometry import ShpPoint
    from shrimp_gis.io import get_utm_detail_from_location
    
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    if _shp_point:
        
        coordinates = _shp_point.coordinates[0]
        location = Location("ShrimpGIS-Location", coordinates[0], coordinates[1], _shp_point.points)
        
        return get_utm_detail_from_location(location)
        
    return None, None, None, None

utm_easting, utm_northing, zone_number, zone_letter = main()


