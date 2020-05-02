# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS Field.
-
Try to export data from other plugin, such as Ladybug and Gismo!
    Args:
        _type_: Type of key to write. Default value is 'C' (character).
        -
        0 = Characters, text.
        1 = Numbers, with or without decimals.
        2 = Floats (same as "N").
        3 = Logical, for boolean values. Required input 0 or 1.
        4 = Dates. Required input format YYYYMMDD.
        5 = Memo, has no meaning within a GIS and is part of the xbase spec instead.
        key_: Name of column. Default value is 'MyField'.
        length_: Length of key. Default is 40.
        decimal_: Number of decimal places found in number key.
        _values: Records (rows) to export to shapefile.
    
    Returns:
        read_me: Message for users.
        field: Column with rows to write within shp file.
"""

ghenv.Component.Name = "ShrimpGIS Field"
ghenv.Component.NickName = "shrimp_field"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "0 || Settings"
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
    from shrimp_gis import Field
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    if _values:
        
        field = Field(_values)
        
        if name_: field.name = name_
        if _type_: field.type = Field.get_type(_type_)
        if length_: field.length = length_
        if decimal_: field.decimal = decimal_
        
        return field
    else:
        return

field = main()
if not field: print("Please, connect values.")
