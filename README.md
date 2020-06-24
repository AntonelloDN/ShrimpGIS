# ShrimpGIS
![Logo](https://github.com/AntonelloDN/ShrimpGIS/blob/master/resources/shrimp_gis_logo.png)
A basic plugin for Grasshopper to read and write shapefile. Read more on [Wiki](https://github.com/AntonelloDN/ShrimpGIS/wiki) pages.
You can use it with other plugins, [example](http://htmlpreview.github.com/?https://github.com/AntonelloDN/ShrimpGIS/blob/master/resources/lb_shrimpgis_threejs_qgis/index.html)
![Alt Text](https://github.com/AntonelloDN/ShrimpGIS/blob/master/examples/ShrimpGIS_milan_top.png)
### Easy to use!
![Alt Text](https://github.com/AntonelloDN/ShrimpGIS/blob/master/examples/shrimp_gis.gif)
![Alt Text](https://github.com/AntonelloDN/ShrimpGIS/blob/master/examples/shrimp_gis_mesh.gif)
![Alt Text](https://github.com/AntonelloDN/ShrimpGIS/blob/master/examples/shrimp_gis_from_img_to_gis.gif)
## Installation:
1. Download ShrimpGIS. Available on [Food4Rhino](https://www.food4rhino.com/app/shrimpgis)
2. Check if downloaded .zip file has been blocked: right click on it, and choose Properties. If there is an Unblock button click on it, otherwise it is OK. Unzip it.
3. Follow 'README.txt' instructions.
## Requirements:
* Rhino 6
## Dependencies:
* pyshp
* utm
## Features:
* Transformation of points, surface/breps, curves, meshes into Esri shapefile entities.
* Discretization for curves and surface/breps.
* Transformation of Esri shapefile entities into points, surface/breps, curves.
* Extraction of fields.
* Write Esri ASCII Raster file.
## Limits v.1.0.1:
* Rhino document has to be in meter
* Only WGS84 (EPSG:4326) reference system is supported. I suggest you use a GIS software for reprojection (e.g. [QGIS](https://www.qgis.org/en/site/)).
* Shapefile read component supports following GIS types:
  * POINT
  * POLYLINE
  * POLYGON
  * POINTZ (imported in GH without z values)
  * POLYLINEZ (imported in GH without z values)
  * POLYGONZ (imported in GH without z values)
## Videos:
[Showcase](https://youtu.be/UY8ezRylcj4)
## Contributors(a-z):
* [Antonello Di Nunzio](https://github.com/AntonelloDN)
### Logo source
Logo is a combination of icons of two designer: [hk12215](https://www.iconfinder.com/hk12215) [strokeicon](https://www.iconfinder.com/strokeicon)


