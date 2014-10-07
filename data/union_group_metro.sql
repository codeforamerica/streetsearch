CREATE TABLE ug_placename
  AS SELECT st_union(geom)
  AS geom, name
  FROM placename
  GROUP BY name;
