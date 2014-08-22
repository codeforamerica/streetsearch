SELECT UpdateGeometrySRID('mesa_boundaries','geom',4269);

DROP TABLE IF EXISTS namedroads;
CREATE TABLE namedroads AS SELECT roadnames.predirabrv as prefix, roadnames.suftypabrv as suffix, roadnames.name as name, roads.fullname as fullname, roads.geom FROM roadnames, roads WHERE roadnames.tlid = roads.tlid;

--
DROP TABLE IF EXISTS mesaroads;
CREATE TABLE mesaroads AS SELECT fullname, namedroads.geom FROM mesa_boundaries, namedroads WHERE ST_DWithin(mesa_boundaries.geom, namedroads.geom, 0);

-- group road rows by name
DROP TABLE IF EXISTS roadlengths;
CREATE TABLE roadlengths as select st_union(geom) as geom, fullname from mesaroads group by fullname;
SELECT UpdateGeometrySRID('roadlengths','geom',4269);
--
-- add column for length
ALTER TABLE roadlengths ADD COLUMN length NUMERIC(12,2);
--
-- populate length of roads
UPDATE roadlengths SET length = ST_Length(ST_Transform(geom,32612));

SELECT fullname, ST_ASText(geom) FROM roadlengths LIMIT 2;

DROP TABLE mesaroads;

CREATE TABLE mesaroads as SELECT * from roadlengths;

DROP TABLE roadlengths;