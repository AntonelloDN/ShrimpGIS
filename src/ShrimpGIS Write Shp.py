# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
It writes ESRI Shapefiles WGS84.
    Args:
        _field_: ShrimpGIS Fields to add to GIS geometries.
        -
        If nothing added to this input, it will be created just one column called UUID.
        _shp_geometry: Geometry to write into shapefile.
        -
        Connect a type of following
        - ShrimpGIS point 
        - ShrimpGIS curve 
        - ShrimpGIS polygon 
        - ShrimpGIS mesh
        _folder: Path of directory where you want to save a shapefile. For example, "C:\Example".
        _name_: Name of shapefile which you want to save on your machine. Default name is <GEOTYPE>.
        run_it_: Set it to True to write shapefile.
    
    Returns:
        read_me: Message for users.
        shp_file: Complete path with extension of the shapefile.
"""

ghenv.Component.Name = "ShrimpGIS Write Shp"
ghenv.Component.NickName = "shrimp_write_shp"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "1 || IO"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
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
    from shrimp_gis.io import ShpWriter
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

warning = Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning

def main():
    
    main_type = _shp_geometry[0].name
    
    name = main_type if _name_ == None else _name_
    
    if None in _field_: print("There is an invalid field."); return
    
    if (run_it_):
        shp_write = ShpWriter()
        result = shp_write.write_shp_file(_folder, name, _shp_geometry, _field_)
        
        if result == False:
                ghenv.Component.AddRuntimeMessage(warning, "Please make sure you are using just one geometry type (e.g. all points) and count of value of fields are equals to geometries count.")
        else:
            return result


shp_file = main() if _shp_geometry and run_it_ and _folder != None else None
if not shp_file:
    print("Add shp_geometry and folder.\nThen set run_it to 'True'.")
else:
    print("File written.")
