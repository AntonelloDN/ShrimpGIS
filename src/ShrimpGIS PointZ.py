# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS PointZ. Use it if you have z values.
    Args:
        _point: Rhino points.
        _location_: ShrimpGIS Location.
    
    Returns:
        shp_point: ShrimpGIS Point [plugin::type::n.point].
"""

ghenv.Component.Name = "ShrimpGIS PointZ"
ghenv.Component.NickName = "shrimp_pointz"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "0 || Settings"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
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
    from shrimp_gis.geometry import ShpPointZ
    from shrimp_gis.io import get_latlon_from_location
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

import scriptcontext as sc
import Grasshopper
import Rhino

warning = Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning

def is_in_meter():
    units = sc.doc.ModelUnitSystem
    if `units` != 'Rhino.UnitSystem.Meters': return False
    return True

def main():
    
    if not is_in_meter():
        ghenv.Component.AddRuntimeMessage(warning, "Rhino model have to be in meter.")
        return
    
    location = Location() if not _location_ else _location_
    
    if _point:
        shp_point = [ShpPointZ(pt) for pt in _point]
        for pt in shp_point:
            pt.coordinates = get_latlon_from_location([pt.geometry], location, True)
        
        return shp_point

shp_point = main()