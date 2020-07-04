# coding=utf-8
"""It contains function to use to transform UTM to WGS84 and vice-versa"""

from ..utm import *
from ..location import Location
import Rhino


def get_utm_detail_from_location(location):
    return from_latlon(location.latitude, location.longitude)


def get_latlon_from_location(pts, location, zvalue=False):

    utmx, utmy, zone, letter = get_utm_detail_from_location(location)
    
    if zvalue:
        utm_pts = [(pt[0] + utmx + location.anchor_point.X, pt[1] + utmy + location.anchor_point.Y, pt.Z + location.altitude) for pt in pts]
        return [list(to_latlon(pt[0], pt[1], zone, letter)) + [pt[2]] for pt in utm_pts]
    else:
        utm_pts = [(pt[0] + utmx + location.anchor_point.X, pt[1] + utmy + location.anchor_point.Y) for pt in pts]
        return [to_latlon(pt[0], pt[1], zone, letter) for pt in utm_pts]


def get_rh_point_from_latlon(point_group, location):

    utmx, utmy, zone, letter = get_utm_detail_from_location(location)
    utm_points = []
    for pts in point_group:

        pts = map(lambda pt: from_latlon(pt[1], pt[0]), pts)
        pts = map(lambda pt: Rhino.Geometry.Point3d(pt[0] - utmx - location.anchor_point.X, pt[1] - utmy - location.anchor_point.Y, 0), pts)

        utm_points.append(pts)

    return utm_points
