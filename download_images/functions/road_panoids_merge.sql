\timing

--stage table for road 20m points
DROP TABLE joins.road_sample_staging;
CREATE TABLE joins.road_sample_staging(
fid integer,
cngmeters double precision,
xcoord double precision,
ycoord double precision
);

--import roads data into table
copy joins.road_sample_staging
FROM PROGRAM 'tail -n +2 /home/emily/phd/urban_perceptions/download_images/outputs/roads/gla_road_points_20m.csv' DELIMITER as ',';

--create roads table
DROP TABLE joins.road_sample;
CREATE TABLE joins.road_sample(
xcoord double precision, 
ycoord double precision,
geog geography(point,4326)
);

--populate table while converting geometry
INSERT INTO joins.road_sample (xcoord, ycoord, geog)
SELECT
   xcoord,
   ycoord,
   ST_Transform(ST_SetSRID(ST_Point(xcoord, ycoord), 4326), 4326) As geog
FROM joins.road_sample_staging;

--create index for faster merging
CREATE INDEX idx_road_sample on joins.road_sample USING gist(geog);

-- create panoids with azimuths staging table.
DROP TABLE joins.panoids_azimuths_staging;
CREATE TABLE joins.panoids_azimuths_staging(
    panoid varchar(30),
    lat double precision, 
    lon double precision,
    month double precision, 
    year double precision,
    azi double precision,
    id varchar(40),
    idx integer
);

--import panoids with azimuths data into staging
copy joins.panoids_azimuths_staging
FROM PROGRAM 'tail -n +2 /home/emily/phd/urban_perceptions/download_images/outputs/psql/test_city_full_azimuth_join.csv' DELIMITER as ',';

--create panoid w/ azimuths table
DROP TABLE joins.panoids_azimuths;
CREATE TABLE joins.panoids_azimuths(
    panoid varchar(30),
    lat double precision, 
    lon double precision,
    geog geography(point,4326),
    month double precision, 
    year double precision,
    azi double precision,
    id varchar(40),
    idx integer
);

--populate table while converting geometry
INSERT INTO joins.panoids_azimuths (panoid, lat, lon, geog, month, year, azi, id, idx)
SELECT
    panoid,
    lat,
    lon,
    ST_Transform(ST_SetSRID(ST_Point(lon, lat), 4326), 4326) As geog,
    month,
    year,
    azi,
    id, 
    idx
FROM joins.panoids_azimuths_staging;

--create index for faster merging
CREATE INDEX idx_panoids_azimuths on joins.panoids_azimuths USING gist(geog);

\COPY (SELECT a.xcoord, a.ycoord, p.panoid, p.lat, p.lon, p.month, p.year, p.azi, p.id, p.idx FROM joins.road_sample As a JOIN LATERAL (SELECT panoid, lat, lon, month, year, azi, id, idx FROM joins.panoids_azimuths AS p ORDER BY a.xcoord, a.geog <-> p.geog LIMIT 1) AS p ON true) to '/home/emily/phd/urban_perceptions/download_images/outputs/psql/test_city_road_sample_panoids.csv' csv header;
COMMIT;
