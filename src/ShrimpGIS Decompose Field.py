# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Use this component to decompose ShrimpGIS Field and extract values.
    
    input:
        _field: Column with rows that comes from "ShrimpGIS Field" or "ShrimpGIS Write Shp".
    output:
        read_me: Message for users.
        name: Name of column.
        values: Records (rows) associated to geometries.
"""

ghenv.Component.Name = "ShrimpGIS Decompose Field"
ghenv.Component.NickName = "shrimp_dec_field"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "1 || IO"
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
    from shrimp_gis.io import ShpReader
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    return ShpReader.decompose_fields(_field)

if (filter(None,_field)):
    values, name = main()
