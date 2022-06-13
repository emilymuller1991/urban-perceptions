-- The goal here is to merge gsv images with azimith angles
-- to determine angle of orientation to download image

CREATE SCHEMA joins;
\timing
CREATE SCHEMA joins;
CREATE EXTENSION Postgis;

--stage a table for azimuth angle data
--gla_aziumuth.csv from step 6
DROP TABLE joins.azimuths_staging;
CREATE TABLE joins.azimuths_staging(
field_1 integer,
xcoord double precision,
ycoord double precision,
azi double precision,
length double precision,
id varchar(40)
);

--stage a table for panoid metadata
--from step 4
DROP TABLE joins.panoids_staging;
CREATE TABLE joins.panoids_staging(
panoid varchar(30),
lat double precision, 
lon double precision,
month double precision, 
year double precision,
idx integer
);

--load azimuths into staged table
copy joins.azimuths_staging
FROM PROGRAM 'tail -n +2 /home/emily/phd/urban_perceptions/download_images/outputs/roads/gla_azimuths.csv' DELIMITER as ',';

--load panoids into staged table
copy joins.panoids_staging
FROM PROGRAM 'tail -n +2 /home/emily/phd/urban_perceptions/download_images/outputs/metadata/test_city_20m_panoids.csv' DELIMITER as ',';


--create final table for azimuths with geometry
DROP TABLE joins.azimuths;
CREATE TABLE joins.azimuths(
field_1 integer,
geog geography(point,4326),
azi double precision,
l double precision,
id varchar(40)
);

--create final table for panoids with geometry
DROP TABLE joins.panoids;
CREATE TABLE joins.panoids(
panoid varchar(30),
lat double precision,
lon double precision,
geog geography(point,4326),
month double precision, 
year double precision,
idx integer
);

--insert staged panoids into panoid table
INSERT INTO joins.panoids (panoid, lat, lon, geog, month, year, idx)
SELECT
    panoid,
    lat, 
    lon,
    ST_Transform(ST_SetSRID(ST_Point(lon, lat), 4326), 4326) As geog,
    month,
    year, 
    idx
FROM joins.panoids_staging;

--insert stages azimuths into azimuth table
INSERT INTO joins.azimuths (field_1, geog, azi, l, id)
SELECT
   field_1,
   ST_Transform(ST_SetSRID(ST_Point(xcoord, ycoord), 27700), 4326) As geog,
   azi,
   length,
   id
FROM joins.azimuths_staging;


CREATE INDEX idx_azimuths on joins.azimuths USING gist(geog);
CREATE INDEX idx_panoids on joins.panoids USING gist(geog);

--This section finds nearest neighbour to azimuth point 
--and merges with panoid. This samples panoids to points
--Need to remove duplicates!

-- https://gis.stackexchange.com/questions/297208/efficient-way-to-find-nearest-feature-between-huge-postgres-tables

-- \COPY (
--     SELECT p.panoid, p.month, p.year, a.azi, a.id 
--     FROM camden.panoids As p 
--     JOIN LATERAL (
--     SELECT azi, id 
--     FROM camden.azimuths AS a 
--     ORDER BY p.panoid, p.geog <-> a.geog 
--     LIMIT 1) 
--     AS a 
--     ON true) 
--     to '/home/emily/phd/002_qgis/psql_outputs/greater_london_panoids_azimuth_join.csv' with header delimiter as ',';

-- For some reason sql not happy with my tab indents in the above example^^

\COPY (SELECT p.panoid, p.lat, p.lon, p.month, p.year, a.azi, a.id, p.idx FROM joins.panoids As p JOIN LATERAL (SELECT azi, id FROM joins.azimuths AS a ORDER BY p.panoid, p.geog <-> a.geog LIMIT 1) AS a ON true) to 'outputs/psql/test_city_full_azimuth_join.csv' csv header;
