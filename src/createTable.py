import psycopg2
import os
import json
from CoverageSearch import CoverageSearchService as QService
import DbManager
from dotenv import load_dotenv

def create_geometry_flex():
    with open("src/Data/geodata2.sql") as file:
        content = file.read()
        # se asume que los comandos estan delimitados por ';'
        commands = content.split(";")
    #connection = None
    try:
        print("Creo tablas")
        connection = DbManager.get_connection()
        cursor = connection.cursor()
        for command in commands:
            command = command.strip()
            #ignoro las lineas vacias
            if not command:
                continue
            cursor.execute(command)
        #cierro comunicacion con el server postgres
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)   

def check_function_flex():
    geojsonCreator = 'SELECT jsonb_build_object(\'type\',     \'FeatureCollection\',\'features\', jsonb_agg(features.feature)) FROM (SELECT jsonb_build_object(\'type\',       \'Feature\',\'id\',         zone_id,\'geometry\',   ST_AsGeoJSON(geom)::jsonb,\'properties\', json_build_object(\'feat_type\', \'Polygon\'  )) AS feature FROM ({}) inputs) features;'
    query = 'SELECT flex.* FROM (SELECT zone_id, geom FROM public.flex_trb) AS flex JOIN (SELECT ST_Buffer(po.geom, 5000, \'quad_segs=8\') as buffer FROM (SELECT ST_POINT({},{})::geography as geom) as po) AS Punto ON ST_Intersects(flex.geom, Punto.buffer)'
    with open("src/Data/puntos1.json") as file:
        jsonFile = json.load(file)
    try:
        print("Creo tablas")
        connection = DbManager.get_connection()
        #cursor = connection.cursor()
        i = 0
        for p in jsonFile['coordinates']:
            jsonText = DbManager.executeQueryAndFetchAll(geojsonCreator.format(query.format(p[0],p[1])), None)
            f = open('src/Data/results/prueba{}.geojson'.format(i), 'w')
            f.write(json.dumps(jsonText[0][0]))
            f.close()
            i = i + 1
        #cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def try_build_db():
    load_dotenv()
    buildDb = os.environ.get("BUILD_DB")
    print(buildDb)
    if (buildDb):
        print(" * Inicia creación de tablas")
        #check_function_flex()
    else:
        print(" * No se crearan las tablas de la base, si así lo desea debe setear el valor BUILD_DB (.env) en 1")

if __name__ == "__main__":
    try_build_db()
