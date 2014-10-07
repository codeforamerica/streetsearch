SELECT UpdateGeometrySRID('mesa_boundaries','geom',4269);

CREATE VIEW namedroads AS SELECT
  roadnames.predirabrv as prefix,
  roadnames.suftypabrv as suffix,
  roadnames.name as name,
  roads.fullname as fullname,
  roads.geom
  FROM roadnames, roads
  WHERE roadnames.tlid = roads.tlid;
--
CREATE VIEW roadswithin=
  AS SELECT fullname, namedroads.geom
  FROM mesa_boundaries, namedroads
  WHERE ST_DWithin(mesa_boundaries.geom, namedroads.geom, 0);

-- group road rows by name
CREATE VIEW roadswithingrouped
  AS SELECT st_union(geom)
  AS geom, fullname
  FROM roadswithin
  GROUP BY fullname;

SELECT fullname, ST_ASGeoJSON(geom) FROM roadswithingrouped WHERE fullname ~ '" + test_string + "'
