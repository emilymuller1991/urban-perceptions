#!/usr/bin/env python3.6.9
import sys

# add plugins path to qgis
sys.path.append("/home/emily/.local/share/QGIS/QGIS3/profiles/default/python/plugins/")
import qgis.utils
from qchainage import chainagetool
from qgis.core import *

# convert road network to points using Qchainage
# Dependencies are Qchainage plugin from QGIS
# and Shapely package: https://github.com/mach0/qchainage


# QGIS STARTUP
# Supply path to qgis install location
qgis.core.QgsApplication.setPrefixPath("/usr", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = qgis.core.QgsApplication([], True)

# Load providers
qgs.initQgis()

# path to original road shape file
path = sys.argv[1]
save = sys.argv[2]
layer = qgis.core.QgsVectorLayer(path, "london_roads")

if not layer.isValid():
    print("Layer failed to load!")
else:
    print("Layer was loaded successfully!")

# input qchainage function
london_road_points = chainagetool.points_along_line(
    layerout="london_road_point",
    startpoint=0,  # of each line segment
    endpoint=-1,  # of each line segment
    distance=20,  # distance to points in each line segment
    label="sampled",
    layer=layer,
    selected_only=False,
    force=False,
    fo_fila=False,
    divide=0,
    decimal=2,
)

points = qgis.core.QgsProject.instance().mapLayersByName("london_road_point")[0]

# check new layer is valid
# layer = QgsVectorLayer(path, 'london_roads')
if not layer.isValid():
    print("Layer failed to load!")
else:
    print("Layer was loaded successfully!")

# Save and Export to CRS 4326
# crsSrc = qgis.utils.iface.activeLayer().crs()
crsDest = qgis.core.QgsCoordinateReferenceSystem(4326)  # WGS 84

# path to save new vector layer
qgis.core.QgsVectorFileWriter.writeAsVectorFormat(
    points, save, "utf-8", crsDest, "ESRI Shapefile"
)

qgs.exitQgis()
