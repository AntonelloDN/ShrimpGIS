# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS Matrix to write Esri ASCII Raster format.
    Args:
        _values: Values to map into a rectangular ASCII matrix [list].
        -
        Values must be from left-right bottom-up.
        How does result should looks like (left-right bottom-up)?
        ...
        5 6 7 8 9
        0 1 2 3 4
        _num_x: Number of pixels at x [int].
        _num_y: Number of pixels at y [int].
    
    Returns:
        ASCII_matrix: ShrimpGIS Matrix.
"""

ghenv.Component.Name = "ShrimpGIS Esri ASCII"
ghenv.Component.NickName = "shrimp_esri_ascii"
ghenv.Component.Message = "1.0.0"
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
    from shrimp_gis.geometry import Matrix
    
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    if _values and _num_x and _num_y:
        matrix = Matrix(_values, _num_x, _num_y)
        
        return matrix
        
    return None

ASCII_matrix = main()


