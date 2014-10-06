SELECT UpdateGeometrySRID('mesa_boundaries','geom',4269);

DROP TABLE IF EXISTS namedroads;
CREATE TABLE namedroads AS SELECT roadnames.predirabrv as prefix, roadnames.suftypabrv as suffix, roadnames.name as name, roads.fullname as fullname, roads.geom FROM roadnames, roads WHERE roadnames.tlid = roads.tlid;

--
DROP TABLE IF EXISTS mesaroads;
CREATE TABLE roadswithin AS SELECT fullname, namedroads.geom FROM mesa_boundaries, namedroads WHERE ST_DWithin(mesa_boundaries.geom, namedroads.geom, 0);

-- group road rows by name
DROP TABLE IF EXISTS roadlengths;
CREATE TABLE roadswithingrouped as select st_union(geom) as geom, fullname from roadswithin group by fullname;
SELECT UpdateGeometrySRID('roadlengths','geom',4269);

DROP TABLE roadswithin;
