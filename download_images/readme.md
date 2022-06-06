# How To Download Google Street View Images

This folder contains all the necessary scripts and steps to take to download Street View Images (GSV) using the Google API. The process can be broken down into the following stages:
1) Download city shape file.
2) Download roads shape file.
3) Create grid points from shape file.
4) Get street view metadata and unique panoramic ids (panoid)
5) Sample points from roads.
6) Add azimuths to road vertices.
7) Merge panoids to azimuths.
8) Merge road points to panoids + azimuths.
9) Download images.

## Sources
Both sources are listed in sources/sources.md.
1) The city shape file is located in source/city_admin/
2) The city roads shape file is located in source/city_roads/

## Get (lat, lon) pairs from admin shape file
The purpose of this step is to sample the shape file at gridded intervals to create 20m spaced (lat,lon) pairs. These will then serve as input to another function to scrape GSV image metadata.

3) Import city shape file in QGIS.
a) Vector > Research Tools > Create Grid: input admin shape file, requires input of horizontal spacing in degrees.
b) Vector > Clip: input grid, clip to admin shape file.
c) Right Click > Export layer > outputs/points/city_20m.csv

## Get GSV metadata
4) In order to make requests to the Google server, we require an API key. When requesting metadata, there is no limit to the number of requests which can be made, although there is a a latency limit. Google provides $200 of credit each month for each API key, allowing a user to download around 25K images for free. Store your API keys in sources/api_keys/ making an original and a copy. The copy will get depleted when running the metadata tasks and must be recopied for each task, subject to cost constraints. The python function which we will use to scrape metadata takes the api_keys file implicitly. 

This step will make use of GNU parallel to speed up processing time. Feeding as input parallel chunks of the (lat, lon) pairs to a python function which then aggregates image metadata into multiple dictionaries. Our main output is a huge dictionary of panoids of the format {'panoid': [lat, lon, month, year]}. The function includes a filter on images which are not owned by Google and which do not have Status: OK.

a) Create a new directory in outputs/metadata/parallel: mkdir parallel. This will store the printed output from the parallel python metadata scrape.
Make sure gnu parallel is installed and run:

* cat outputs/points/city_20m.csv | parallel --delay 1.5 --joblog /tmp/log --progress --pipe --block 3M --files --tmpdir outputs/metadata/parallel python3 functions/parallel_grid.py 
* cat outputs/points/greater_london_20m.csv | parallel --delay 1.5 --joblog /tmp/log --progress --pipe --block 3M --files --tmpdir outputs/metadata/parallel python3 functions/parallel_grid.py 
cat outputs/points/greater_london_20m.csv | parallel --delay 1.5 --joblog /tmp/log --progress --pipe --block 3M --ungroup python3 functions/parallel_grid.py 

outputs/city_20m.csv is stdin.
parallel calls gnu parallel
--delay 1.5 creates a 1.5 second delay in sending each parallel chunk to be processed. This is used to feed in each API key.
--joblog prints log to '/tmp/log' and tells the time (important! copy and paste into city folder after execution!)
--progress prints job progress to terminal
--block 1M splits stdin into 1M size chunks (make sure there are enough API keys for each block or make blocks bigger)
--files prints location
--tmdir points to save location of output files
python3 parallel_grid.py calls the function to be executed.
!NB for dev, removes --files -tmpdir... and replace with --ungroup and retrieve output to terminal.

b) Create a new directory in outputs/metadata/years: mkdir years. This will store the aggregated output of the parallel script separated by years.
run: python3 functions/parallel_output.py city_20m outputs/metadata/parallel/ /outputs/metadata/
The first argument is used as the city name to title the files. The second argument is where to find parallel metadata output and the third argument is where to save new aggregated metadata.

Once the jsons and csv's have been created from the .py, copy the .csv summary data into a new tab in the file summary_files.ods.
Copy the replicates and total # of yearly unique panoids into the .csv file. 
Remember to grab the log from tmp/log

## Sample points from roads
This function will sample 20m distance points along all roads in the city. The function uses the pyQGIS module and requires 

5) run python3 get_road_points.py source/coty_roads/city_streets.shp outputs/roads/city_road_points_20m.shp
The first argument inputs road shape file location and the second argument passes save file and location.

## Add Azimuth to Road Vertices
One step in data cleaning is to get the azimuth angle of the road to north bearing. This will then serve as a rotation of camera input when we download the images. This will be necessary since inputting standard 90 degrees is often offset and does not give a perpindicular angle to the road.

6) Import city_roads shape file into QGIS
a) Vector > Geometry > Extract Vertices: input city_road.shp
b) Vector > Geometry > Add Geometry Attributes: input output from previous step
c) Export layer > outputs/roads/city_road_vertices_geom.csv

In the final step we will call the function azimuth.py to get azimuth angles from vertices in shape file and merge back to our exported layer.

d) run python3 azimuth.py source/city_roads/city_streets.shp outputs/roads/city_road_vertices_geom.shp outputs/roads/
the first argument is the location of the streets shape file, the second argument is the location of out last output and third argument is save location of our new azimuth file.

## Merge panoids to Azimuth
The final steps utilises psql to merge panoid metadata to azimuths to serve as input for download. It requires the installation of postgres. Once you have downloaded postgres and created user, create database as follows:

sudo su - postgres
psql
CREATE DATABASE city;

7) run: psql -U user -d city -f /home/emily/phd/0_get_images/functions/panoids_azimuth_merge.sql.

psql -U emily -d london -f /home/emily/phd/0_get_images/functions/panoids_azimuth_merge_census_2021.sql.

## Merge road points to panoids + azimuths
The next step is to ensure one area is not over sampled, and furthermore, have an approximation of GSV road coverage. 

8a) run psql -U user -d city -f /home/emily/phd/0_get_images/functions/roads_panoids_merge.sql

run psql -U emily -d london -f /home/emily/phd/0_get_images/functions/road_panoids_merge_apr_2021.sql
* NEED TO INCLUDE HERE ADDING IDX.
# remove duplicate IDs

## Download Images
Now we can download the images using the final output from the previous step, python and gnu parallel. Remember to copy back the original api_keys_original.csv to api_keys.csv.
We will first convert the .csv to plain text as follows:

9a) run: split -l 40000000 -d greater_london_2015_panoids_to_download.csv ../to_download/london2015
from london2015 remove the header manually. 

b) run: cat outputs/psql/london20m | parallel --delay 1.5 --joblog /tmp/log --pipe --block 2M --ungroup python3 functions/get_images.py

cat outputs/to_download/2018/201800 | parallel --delay 1.5 --joblog /tmp/log --pipe --block 2M --ungroup python3 functions/get_images.py 


This function will download 2 angles per panoid, facing either side of the street. Make sure that 2MB remains below the 25K images per month quota. This can take days depending on how many images you have sent to the server and it is likely that errors will occur.
