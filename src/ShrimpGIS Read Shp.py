# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Use this component to read shapefiles.
-
Supported shapefile types are:
    1) POINT
    2) POLYLINE
    3) POLYGON
    4) POINTZ
    5) POLYLINEZ
    6) POLYGONZ
-
Remark: Only WGS84 (EPSG:4326) reference system is supported.
If your shp use another coordinate system you have to reproject it using a GIS software (e.g. QGIS).

    Args:
        _shp_file: Complete path with extension of a shapefile. E.g. C:\Example\shapefile.shp
        _location_: ShrimpGIS Location.
        run_it_: Set it to true to run component.
    Returns:
        read_me: Message for users.
        field: ShrimpGIS Fields attached to GIS geometries.
        geometry: Imported geometries in Rhino world.
        -
        They are arranged in GH tree in "Maintain" mode. Branches of missing geometries are deleted automatically.
        -------------------:
        missing_geometry: Some geometries can be not import correctly. Here you can find Id of missing geometries.
        -
        Use this output to create Paths or use it as List to clear Field values from missing geometries.
"""

ghenv.Component.Name = "ShrimpGIS Read Shp"
ghenv.Component.NickName = "shrimp_read_shp"
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
    from shrimp_gis import __version__, Location
    from shrimp_gis.io import ShpReader
    from shrimp_gis.io import from_nested_lat_lon_to_utm
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################


def main():
    
    level = Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark
    
    if not _shp_file:
        print("Connect a compatible shapefile to read.\nThen set run_it to 'True'.")
        return [None]*3
    
    location = Location() if not _location_ else _location_
    
    if run_it_:
        
        reader = ShpReader(_shp_file)
        
        if (reader.level == "not supported"):
            ghenv.Component.AddRuntimeMessage(level, "I am Sorry, {0} file type is not supported" \
            " by shp reader components.".format(reader.type_name))
            return [None]*3
        else:
            gh_points = from_nested_lat_lon_to_utm(reader.points, location)
            
            if (reader.level == "supported with z"):
                ghenv.Component.AddRuntimeMessage(level, "{0} file type supported." \
                " This shp file has Z values.".format(reader.type_name))
                
                for pts, zs in zip(gh_points, reader.z):
                    for pt, z in zip(pts, zs):
                        pt.Z = z - location.altitude
            
            geometry, missing_geometry = reader.get_georeferenced_rhino_geometry(gh_points)
            field = reader.fields
            
            return field, geometry, missing_geometry
        
    else:
        return [None]*3

field, geometry, missing_geometry = main()

