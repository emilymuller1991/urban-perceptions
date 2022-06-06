#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Downloading Google Metadata
                             A GNU parallel python programme

 Obtains unqiue image panoids from Goole Street View API

 Usage from command line:
 cat points/city_50m.csv | parallel --delay 1.5 --joblog /tmp/log --progress /
 --pipe --block 1M --files --tmpdir cities/city/parallel python3 python/parallel_grid.py
                              -------------------
        begin                : 2019-13-12
        copyright            : (C) 2014 by Emily Muller
        email                : emily.muller@imperial.ac.uk
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import fileinput
import time
from typing import Dict

import numpy as np
import utils

# ~~~ GLOBAL VARIABLES ~~~#
# create two dictionary items
all_gps: Dict[str, list] = {}  # {"lat,lon": [panoids]}
all_pano: Dict[str, Dict] = {}  # {panoids: [metadata]}

gps = 0
start_time = time.time()

# GET API KEY one by one
api_key = utils.get_api("source/api_keys/api_keys.csv")

# Run Programme in parallel with API Key
for line in fileinput.input():
    gps += 1
    try:
        if fileinput.isfirstline():
            file = fileinput.filename()
        else:
            # get lat and lon
            x, y = utils.dont_convert_line(line)
            # update dictionary with scraped metadata
            utils.get_panoids(x, y, all_gps, all_pano, api_key)

    except Exception as e:
        print("Metadata not downloading with error: %s" % e)
        continue
end_time = time.time()

print(all_pano)
print(all_gps)

try:
    number_of_images_per_point = [len(all_gps[key]) for key in all_gps.keys()]
    zeros = number_of_images_per_point.count(0)
    points = gps
    print(
        "Number of points: %s" % str(points),
        "Number of unique pano IDs: %s " % len(all_pano.keys()),
        "Number of points with no images: %s" % number_of_images_per_point.count(0),
        "Average non-zero images per point: %s"
        % (sum(number_of_images_per_point) / (len(number_of_images_per_point) - zeros)),
        "Average images per point: %s " % np.mean(number_of_images_per_point),
        "Total time: %s" % str(end_time - start_time),
    )
except Exception as e:
    print("Failed to print summary " + str(e))
