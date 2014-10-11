CREATE TABLE ug_placename
  AS SELECT st_union(geom)
  AS geom, fullname
  FROM placename
  GROUP BY name;
