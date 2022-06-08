# get azimuth angles for each feature in a layer.
# Dependencies are Azimuth QGIS python plugin package:
# https://github.com/lcoandrade/AzimuthDistanceCalculator/blob/master/azimuthsAndDistances/azimuthsAndDistances.py

import sys

# add plugins path
sys.path.append("/home/emily/.local/share/QGIS/QGIS3/profiles/default/python/plugins/")
import time

import pandas as pd
import qgis.utils
from AzimuthDistanceCalculator.azimuthsAndDistances import azimuthsAndDistances
from qgis.core import *

# QGIS STARTUP
# Supply path to qgis install location
qgis.core.QgsApplication.setPrefixPath("/usr", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = qgis.core.QgsApplication([], True)

# Load providers
qgs.initQgis()

# data cleaning functions


def get_latlon(point):
    x = point[0]
    y = point[1]
    return x, y


def get_azimuth(calc):
    len = calc[0]
    azi = calc[1]
    return len, azi


# path to original road shape file
road_path = sys.argv[1]
geom_path = sys.argv[2]
save_roads = sys.argv[3]

layer = qgis.core.QgsVectorLayer(road_path, "london_roads")

if not layer.isValid():
    print("Layer failed to load!")
else:
    print("Layer was loaded successfully!")

# get azimuth angle
start_time = time.time()
f_count = 0
azimuths = {}
features = layer.getFeatures()
for feature in features:
    f_count += 1
    azi = azimuthsAndDistances.AzimuthsAndDistancesDialog(feature, feature.geometry())
    azi.isValidType()
    points = azi.points
    calcs = azi.calculate()
    for i in range(len(calcs)):
        x, y = get_latlon(points[i])
        l, azi = get_azimuth(calcs[i])
        azimuths[str(feature.id()) + str(i)] = [x, y, azi, l, feature.attributes()[1]]
    print("Completed feature %s in time %s" % (f_count, time.time() - start_time))

# save as df
df = pd.DataFrame(azimuths).T
df.columns = ["xcoord", "ycoord", "azi", "l", "id"]
print(df.head())
df.to_csv(save_roads + "gla_azimuths.csv")

# merge to geom layer
starting_merge = time.time()
df_vertices = pd.read_csv(geom_path)
merged = df_vertices.merge(df, on=["xcoord", "ycoord"], how="outer")
print(merged.head())
merged.to_csv(save_roads + "gla_geometery_azimuths.csv")
end_time = time.time()
print("Completed merge in %s seconds" % (end_time - starting_merge))
