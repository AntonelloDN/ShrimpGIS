# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS Curve.
    Args:
        _surface: A Rhino or Grasshopper Curve to export.
        _location_: ShrimpGIS Location.
        _num_: Number of point to consider for discretization of curves. If it is a polyline component automatically recognizes points.
        -
        Default value is 10.
    
    Returns:
        shp_curve: ShrimpGIS Curve [plugin::type::n.point].
"""

ghenv.Component.Name = "ShrimpGIS Curve"
ghenv.Component.NickName = "shrimp_curve"
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
    from shrimp_gis.geometry import ShpCurve
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
    num = 10 if not _num_ else _num_
    
    if _curve:
        shp_curve = [ShpCurve(crv, num) for crv in _curve]
        for geo in shp_curve:
            geo.coordinates = get_latlon_from_location(geo.points, location)
        
        return shp_curve

shp_curve = main()
