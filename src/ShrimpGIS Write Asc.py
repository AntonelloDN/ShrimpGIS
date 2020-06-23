# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
It writes Esri ASCII Raster.
-
It is a raster format file you can open with QGIS, for example.
    Args:
        _ASCII_matrix: ShrimpGIS ASCII matrix.
        _pixel_size: Dimension (Length or Width) in meter of pixel [float].
        _utm_easting: Easting value of UTM coordinate [float].
        _utm_northing: Northing value of UTM coordinate [float].
        _prj_text: Text to write into *.prj file. Connect output of 'ShrimpGIS UTM PRJ'.
        _folder: Path of directory where you want to save asc file. For example, "C:\Example".
        _name_: Name of asc which you want to save on your machine. Default name is 'shrimp_gis_asc'.
        run_it_: Set it to True to write asc file.
    
    Returns:
        read_me: Message for users.
        asc_file: Complete path with extension of the raster file.
"""

ghenv.Component.Name = "ShrimpGIS Write Asc"
ghenv.Component.NickName = "shrimp_write_asc"
ghenv.Component.Message = "1.0.0"
ghenv.Component.Category = "ShrimpGIS"
ghenv.Component.SubCategory = "1 || IO"
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
    from shrimp_gis.io import AscWriter
    
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################


def main():
    
    name = "shrimp_gis_asc" if _name_ == None else _name_
    
    if _ASCII_matrix and _pixel_size and _utm_easting and _utm_northing and _prj_text and _folder and run_it_:
        
        asc_file = AscWriter(_ASCII_matrix, _pixel_size, _utm_easting, _utm_northing)
        file = asc_file.get_asc(_folder, name, _prj_text)
        
        return file
        
    return

asc_file = main()
if not asc_file: print("Please, connect _ASCII_matrix, _pixel_size, _utm_easting, _utm_northing, _prj_text, _folder and set run_it_ to 'True'.")


