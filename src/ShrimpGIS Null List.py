# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Utility to create NULL list.
-
Use it when you want to add NULL value to Shp Fields.
    Args:
        _number: Number of NULL values to create.
    
    Returns:
        null_list: List of NULL.
"""

ghenv.Component.Name = "ShrimpGIS Null List"
ghenv.Component.NickName = "shrimp_null_list"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "0 || Utils"
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
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    if _number:
        
        return [None] * _number
    else:
        return

null_list = main()
