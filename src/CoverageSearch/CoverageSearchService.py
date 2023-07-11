from flask import jsonify
import DbManager
import psycopg2

def searchCoverageByPointAndRadius(lat,lon,radius):
    query = 'SELECT flex.zone_id FROM (SELECT zone_id, geom FROM public.flex_trb) AS flex JOIN (SELECT ST_Buffer(po.geom, {}, \'quad_segs=8\') as buffer FROM (SELECT ST_POINT({},{})::geography as geom) as po) AS Punto ON ST_Intersects(flex.geom, Punto.buffer)'.format(radius,lon,lat)
    try:
        coverage = DbManager.executeQueryAndFetchAll(query, None)
        if coverage == None or len(coverage) == 0:
            return None
        else:
            return coverage
    except (Exception, psycopg2.DatabaseError) as error:
        return {"error": "No se pudo encontrar cobertura para el punto y radio ingresado."}
