# coding=utf-8
"""
Query to get EPSG code and other info. It uses epsg.io and 'what's my UTM zone' website formula.
"""

from System.Net import WebClient

def get_epsg_from_shp_point(shp_point):
    """UTM zone starting at zone 1 from -180°E to -174°E"""

    coordinates = shp_point.coordinates[0]
    return int(32700-round((45 + coordinates[0])/90,0)*100+round((183 + coordinates[1])/6,0))


def get_prj_text_from_EPSG(EPSG):
    """Get prj string by epsg.io using .Net."""

    path = "https://epsg.io/" + str(EPSG) + ".wkt"
    web_client = WebClient()
    try:
        web_client.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)")
        prj_text = web_client.DownloadString(path)
    except:
        raise Exception("Query failed. Please, copy and paste https://epsg.io/?{0}.wkt on your browser, check if text is showed. If yes, use it with gh.".format(EPSG))

    return prj_text