--
CREATE TABLE roadnames AS SELECT featnames.predirabrv as prefix, featnames.suftypabrv as suffix, featnames.name as name, roads.fullname as fullname, roads.geom FROM featnames, roads WHERE featnames.tlid = roads.tlid;

-- group road rows by name
CREATE TABLE roadlengths as select st_union(geom) as geom, fullname from roads group by fullname;
--
-- add column for length
ALTER TABLE roadlengths ADD COLUMN length NUMERIC(12,2);
--
-- populate length of roads
UPDATE roadlengths SET length = ST_Length(ST_Transform(geom,32612));

SELECT fullname, ST_ASGeoJSON(geom) FROM roadlengths LIMIT 2;
