# ShrimpGIS: A basic plugin to read and write shapefile (GPL).
# This file is part of ShrimpGIS.
#
# Copyright (c) 2020, Antonello Di Nunzio <antonellodinunzio@gmail.com>.
# You should have received a copy of the GNU General Public License
# along with ShrimpGIS; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Construct a ShrimpGIS Location.
    Args:
        name: Name of Location.
        latitude: Latitude of Location WGS84 [float].
        longitude: Longitude of Location WGS84 [float].
        anchor_point: Rhino point to use as anchor point of Location.
    
    Returns:
        location: ShrimpGIS Location.
"""

ghenv.Component.Name = "ShrimpGIS Location"
ghenv.Component.NickName = "shrimp_location"
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
    from shrimp_gis import Location
    ghenv.Component.Message = __version__
except ImportError as e:
    raise ImportError("\nFailed to import ShrimpGIS: {0}\n\nCheck your 'shrimp_gis' folder in {1}".format(e, os.getenv("APPDATA")))
################################################

def main():
    
    location = Location()
    
    if _name_: location.name = _name_
    if _latitude_: location.latitude = _latitude_
    if _longitude_: location.longitude = _longitude_
    if _anchor_point_: location.anchor_point = _anchor_point_
    
    return location

location = main()
