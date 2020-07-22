# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Use this component to read geojson file.
-
Supported geojson types are:
    1) Point
    2) MultiPoint
    3) LineString
    4) MultiLineString
    5) Polygon
    6) MultiPolygon
-
More info about geojson compliant structure supported by ShrimpGIS here: https://en.wikipedia.org/wiki/GeoJSON
-
Remark: Only WGS84 (EPSG:4326) reference system is supported.
The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS84) datum, with longitude and latitude units of decimal degrees. This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.
-
reference: https://cran.r-project.org/web/packages/geojsonio/vignettes/geojson_spec.html
    Args:
        _geojson_file_: Complete path with extension of a geojson file. E.g. C:\Example\my_json.json
        -
        Note it supports geojson standard rfc7946. To see compatible structure see here: https://en.wikipedia.org/wiki/GeoJSON
        _location_: ShrimpGIS Location.
        run_it_: Set it to true to run component.
    Returns:
        read_me: Message for users.
        field: ShrimpGIS Fields attached to GIS geometries.
        type: Imported geojson type in Rhino world.
        -
        Note that a geojson file supports multiple geometry type at the same time.
        geometry: Imported geometries in Rhino world.
"""

ghenv.Component.Name = "ShrimpGIS Read Geojson"
ghenv.Component.NickName = "shrimp_read_geojson"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "1 || IO"
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import os
import sys
import Grasshopper
import Rhino
import System

##################ShrimpGIS#####################
try:
    user_path = os.getenv("APPDATA")
    sys.path.append(user_path)
    from shrimp_gis import __version__, Location
    from shrimp_gis.io import GeojsonReader
    from shrimp_gis import Field
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################


def main():
    
    if run_it_:
        location = Location() if not _location_ else _location_
        
        reader = GeojsonReader(_geojson_file_)
        geometry = reader.get_georeferenced_rhino_geometry(location)
        
        return reader.fields, reader.type, geometry
    return [None]*3

field, type, geometry = main()
