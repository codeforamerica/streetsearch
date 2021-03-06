-- creates a view with road names and geometries
CREATE VIEW namedroads
  AS SELECT roadnames.predirabrv as prefix,
  roadnames.suftypabrv as suffix,
  roadnames.name as name,
  roads.fullname as fullname,
  roads.geom
  FROM nameid as roadnames, edgeid as roads
  WHERE roadnames.tlid = roads.tlid;

--creates a view with road names and geometries within city boundaries
CREATE VIEW roadswithin
  AS SELECT fullname, namedroads.geom
  FROM placetableid as boundaries, namedroads
  WHERE ST_DWithin(boundaries.geom, namedroads.geom, 0);

-- group road rows by name
DROP TABLE IF EXISTS uplacetableid;
CREATE TABLE uplacetableid
  AS SELECT st_union(geom)
  AS geom, fullname
  FROM roadswithin
  GROUP BY fullname;

DROP VIEW roadswithin;
DROP VIEW namedroads;
