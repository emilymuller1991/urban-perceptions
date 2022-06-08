import ast
import os
import sys
from ast import literal_eval
from typing import Dict

import numpy as np
import pandas as pd

city = sys.argv[1]
parallel = sys.argv[2]
save = sys.argv[3]

os.chdir(parallel)
files = os.listdir()


def make_summary_dict(file, data):
    splits = data.split(" ")
    return {
        file: [
            int(splits[3]),
            int(splits[9]),
            int(splits[17]),
            np.float(splits[23]),
            np.float(splits[28]),
            np.float(splits[32]),
        ]
    }


# GET INFORMATION FROM PARALLEL FILES #
# create two dictionary items

# summary csv
summary: Dict[str, list] = {}
# {'file':["# points", "# unique panoids",
# "# images", "avg img/point", "# non google", "time (s)",]}

# all panoids dictionary
panoids: Dict[str, Dict] = {}
# {'panoids': {lat, lon, year, month} }

# all points dictionary
points: Dict[str, list] = {}  # {'(lat,lon)': [panoids]}
no_points: Dict[str, list] = {}  # {'(lat,lon)': []}

# list of all duplicates
duplicates = []

# iterate through each file in the folder
for file in files:
    with open(file) as f:
        data = f.read().splitlines()
        data = data[-3:]
        try:
            summary = dict(summary, **make_summary_dict(file, data[2]))
            file_panoids = ast.literal_eval(data[0])
            file_points = ast.literal_eval(data[1])
            dup = set(panoids.keys()).intersection(set(file_panoids.keys()))
            duplicates.append(dup)
            for point in file_points:
                if set(file_points[point]) - dup != 0:
                    file_points[point] = list(set(file_points[point]) - dup)
                if len(file_points[point]) == 0:
                    no_points[point] = []
            panoids = dict(panoids, **file_panoids)
            points = dict(points, **file_points)
        except Exception as e:
            print("This file has no images:" + file)
            print("Error: %s" % str(e))

# GET INFORMATION FROM PARALLEL FILES #
print(len(panoids.keys()))
print(len(points.keys()))
print(len(no_points.keys()))
print(summary)
# SAVE INFORMATION FROM PARALLEL FILES #
# save all co-ordinates to dataframe
co_ords = [literal_eval(key) for key in no_points.keys()]
co_ords_ = list(zip(*co_ords))
no_points_df = pd.DataFrame(co_ords_).T
no_points_df.to_csv("%s%s_no_points.csv" % (save, city))

# save all co-ordinates to dataframe
co_ords = [literal_eval(key) for key in points.keys()]
co_ords_ = list(zip(*co_ords))
points_df = pd.DataFrame(co_ords_).T
points_df.to_csv("%s%s_points.csv" % (save, city))

# save all panoids to dataframe
panoids_df = pd.DataFrame(panoids).T
panoids_df.columns = ["lat", "lon", "month", "year"]
panoids_df["img_id"] = np.arange(0, panoids_df.shape[0])
panoids_df.to_csv("%s%s_panoids.csv" % (save, city))

# Total number of replicates
replicates = sum([len(dup) for dup in duplicates])
print("A total of %s replicates have been detected in the parallel files" % replicates)

# Total number of panoids in point dict
total = 0
for point in points:
    total += len(points[point])
print("There are a total of %s unique panoids" % total)

# create yearly dataframe
k6: Dict[str, Dict] = {}  # {'panoids': {lat, lon, year, month} }
k7: Dict[str, Dict] = {}
k8: Dict[str, Dict] = {}
k9: Dict[str, Dict] = {}
k10: Dict[str, Dict] = {}
k11: Dict[str, Dict] = {}
k12: Dict[str, Dict] = {}
k13: Dict[str, Dict] = {}
k14: Dict[str, Dict] = {}
k15: Dict[str, Dict] = {}
k16: Dict[str, Dict] = {}
k17: Dict[str, Dict] = {}
k18: Dict[str, Dict] = {}
k19: Dict[str, Dict] = {}
k20: Dict[str, Dict] = {}
k21: Dict[str, Dict] = {}
years = [k7, k8, k9, k10, k11, k12, k13, k14, k15, k16, k17, k18, k19, k20, k21]
for pano in panoids:
    if panoids[pano]["year"] == 2011:
        k11[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2012:
        k12[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2013:
        k13[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2014:
        k14[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2015:
        k15[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2016:
        k16[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2017:
        k17[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2018:
        k18[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2010:
        k10[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2009:
        k9[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2008:
        k8[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2007:
        k7[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2006:
        k6[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2019:
        k19[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2020:
        k20[pano] = panoids[pano]
    elif panoids[pano]["year"] == 2021:
        k21[pano] = panoids[pano]

# save yearly csv's.
y = 2007
for year in years:
    yearly_df = pd.DataFrame(year).T
    yearly_df.to_csv("%syears/%s_panoids_%s.csv" % (save, city, y))
    y += 1
print(
    len(k6.keys()),
    len(k7.keys()),
    len(k8.keys()),
    len(k9.keys()),
    len(k10.keys()),
    len(k11.keys()),
    len(k12.keys()),
    len(k13.keys()),
    len(k14.keys()),
    len(k15.keys()),
    len(k16.keys()),
    len(k17.keys()),
    len(k18.keys()),
    len(k19.keys()),
    len(k20.keys()),
    len(k21.keys()),
)

# save file summary to csv
df = pd.DataFrame(summary).T
df.columns = [
    "# points",
    "# unique panoids",
    "# images",
    "avg img/point",
    "# non google",
    "time (s)",
]
df.to_csv("%s%s_file_summary.csv" % (save, city))
