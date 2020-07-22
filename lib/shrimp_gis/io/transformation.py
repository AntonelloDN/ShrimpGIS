# coding=utf-8
"""It contains function to use to transform UTM to WGS84 and vice-versa"""

from ..utm import *
from ..location import Location
import Rhino


def get_utm_detail_from_location(location):
    return from_latlon(location.latitude, location.longitude)


def get_latlon_from_location(pts, location, zvalue=False):

    location.set_utm()
    
    if zvalue:
        utm_pts = [(pt[0] + location.utmx + location.anchor_point.X, pt[1] + location.utmy + location.anchor_point.Y, pt.Z + location.altitude) for pt in pts]
        return [list(to_latlon(pt[0], pt[1], location.zone, location.letter)) + [pt[2]] for pt in utm_pts]
    else:
        utm_pts = [(pt[0] + location.utmx + location.anchor_point.X, pt[1] + location.utmy + location.anchor_point.Y) for pt in pts]
        return [to_latlon(pt[0], pt[1], location.zone, location.letter) for pt in utm_pts]


def from_lat_lon_to_utm(points, location):

    points = map(lambda pt: from_latlon(pt[1], pt[0]), points)

    return map(lambda pt: Rhino.Geometry.Point3d(pt[0] - location.utmx - location.anchor_point.X, pt[1] - location.utmy - location.anchor_point.Y, 0), points)


def from_nested_lat_lon_to_utm(point_group, location):

    location.set_utm()

    utm_points = []
    for pts in point_group:
        utm_points.append(from_lat_lon_to_utm(pts, location))

    return utm_points


