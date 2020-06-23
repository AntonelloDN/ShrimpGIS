# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Get EPSG code and *.prj content for a specific Shrimp point. Use it with 'ShrimpGIS Write Asc'.
-
This component uses internet connection. It retrieves PROJCS string of UTM (datum WGS84).
-
EPSG code is an ID between 1024-32767 which is part of a public registry of spatial reference systems (EPSG registry).
PRJ file contains the projected coordinate system you are referring to. It is an important file to map correctly raster file as well vector files.
    Args:
        _shp_point: Shrimp point to use to get UTM projection reference system.
    
    Returns:
        EPSG: EPSG code.
        prj_text: Text to write into a *.prj file. Connect it to 'ShrimpGIS Write Asc'.
"""

ghenv.Component.Name = "ShrimpGIS UTM PRJ"
ghenv.Component.NickName = "shrimp_utm_prj"
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
    from shrimp_gis.io import get_epsg_from_shp_point, get_prj_text_from_EPSG
    
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    if _shp_point:
        EPSG = get_epsg_from_shp_point(_shp_point)
        prj_text = get_prj_text_from_EPSG(EPSG)
        
        return EPSG, prj_text
    return None, None

EPSG, prj_text = main()


