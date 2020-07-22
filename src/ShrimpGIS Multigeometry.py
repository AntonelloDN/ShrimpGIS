# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS MultiGeometry to use with geojson. It puts many geometry entities of the same family together.
-
REMARK: For Geojson only!
    Args:
        _shp_geometry: Connect a list of ShpCurves or ShpPoints or ShpSurfaces [list].
        
    Returns:
        shp_multi: ShrimpGIS MultiGeometry [plugin::type("multi" + type)::n.geometries].
"""

ghenv.Component.Name = "ShrimpGIS MultiGeometry"
ghenv.Component.NickName = "shrimp_multi_geometry"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "0 || Settings"
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass

import scriptcontext as sc
import os
import sys
##################ShrimpGIS#####################
try:
    user_path = os.getenv("APPDATA")
    sys.path.append(user_path)
    from shrimp_gis import __version__
    from shrimp_gis.geometry import MultiGeometry
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
    
    if _shp_geometry:
        shp_multi = MultiGeometry(_shp_geometry)
        
        return shp_multi

shp_multi = main()
