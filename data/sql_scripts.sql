--Intersects
SELECT flex.zone_id
FROM (SELECT zone_id, geom FROM public.flex_trb) AS flex
JOIN (SELECT ST_Buffer(po.geom, 5000, 'quad_segs=8') as buffer FROM (SELECT ST_POINT(-58.513626,-34.510756,4326)::geography as geom) as po) AS Punto
ON ST_Intersects(flex.geom, Punto.buffer);

--distance
SELECT flex.zone_id,ST_Distance(flex.centroide, Punto.geom)
FROM (SELECT zone_id, ST_Centroid(geom)::geography as centroide FROM public.flex_trb) AS flex
JOIN (SELECT ST_POINT(-58.513626,-34.510756,4326)::geography as geom) AS Punto
ON ST_Distance(flex.centroide, Punto.geom) < 5000;

--distance of all points of TRB geojson
SELECT flex.zone_id,ST_AsText(flex.centroide) as centroide ,ST_Distance(flex.centroide, flex.punto) as distance
FROM (SELECT zone_id, ST_Centroid(geom)::geography as centroide,ST_POINT(-58.513626,-34.510756,4326)::geography as punto FROM public.flex_trb) AS flex

--create geojson from query
SELECT jsonb_build_object(
    'type',     'FeatureCollection',
    'features', jsonb_agg(features.feature)
)
FROM (
  SELECT jsonb_build_object(
    'type',       'Feature',
    'id',         zone_id,
    'geometry',   ST_AsGeoJSON(geom)::jsonb,
    'properties', json_build_object(
        'feat_type', 'Polygon'
     )
  ) AS feature
  FROM (SELECT * FROM public.flex_trb) inputs) features;

--create geojson from buffer (only one polygon)
SELECT json_build_object(
    'type',       'Feature',
    'id',         'buffer',
    'geometry',   ST_AsGeoJSON(foo.buffer)::json,
    'properties', json_build_object(
        'feat_type', 'Polygon'
     )
 )
 FROM (SELECT ST_Buffer(po.geom, 5000, 'quad_segs=8') as buffer FROM (SELECT ST_POINT(-58.513626,-34.510756,4326)::geography as geom) as po) AS foo;