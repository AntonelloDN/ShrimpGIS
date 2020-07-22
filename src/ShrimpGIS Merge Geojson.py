# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
This is a special component that merges together geojson files with features into a new file.
-
It is very helpful if you work with separate and massive geojson and then you want to create just one file for them.
E.g. a point layer with information about trees; a polygon layer with information about building and so on.
    Args:
        _geojson_file: geojson files to merge.
        -
        Standard rfc7946. Reference here: https://en.wikipedia.org/wiki/GeoJSON
        _folder: Path of directory where you want to save geojson file. For example, "C:\Example".
        _name_: Name of geojson which you want to save on your machine. Default name is "Geojson".
        run_it_: Set it to True to write geojson.
    
    Returns:
        read_me: Message for users.
        geojson_file: Complete path with extension of the new geojson.
"""

ghenv.Component.Name = "ShrimpGIS Merge Geojson"
ghenv.Component.NickName = "shrimp_merge_geojson"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "1 || IO"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

import scriptcontext as sc
import os
import sys
import Grasshopper
import Rhino

##################ShrimpGIS#####################
try:
    user_path = os.getenv("APPDATA")
    sys.path.append(user_path)
    from shrimp_gis import __version__
    from shrimp_gis.io import GeojsonWriter
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

warning = Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning

def main():
    
    name = "Geojson" if _name_ == None else _name_
    
    if (run_it_):
        result = GeojsonWriter.merge_geojson(_folder, name, _geojson_file)
        
        return result


geojson_file = main() if _geojson_file and run_it_ and _folder != None else None
if not geojson_file:
    print("Add _geojson_file and folder.\nThen set run_it to 'True'.")
else:
    print("File written.")
