import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import DatabaseError


def get_connection():
    try:
        load_dotenv()  
        dbName = os.environ.get("DATABASE_NAME") 
        dbUser = os.environ.get("DATABASE_USER")
        dbPass = os.environ.get("DATABASE_PASS")
        dbPort = os.environ.get("DATABASE_PORT") 
        connection = psycopg2.connect(database=dbName, user = dbUser, password = dbPass, port=dbPort)
        return connection
    except DatabaseError as ex:
        raise ex
    
def executeQueryAndFetchAll(query, whereTuple):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, whereTuple)
            geom = cursor.fetchall()
        return geom
    except Exception as ex:
        raise Exception(ex)
    finally:
        conn.close()

def executeInsertQuery(QUERY, valuesTuple):
    try:
        print("### Abro Conexion ###")   
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(QUERY, valuesTuple)    
            conn.commit()  
            id = cursor.fetchone()[0]        
        return id
    except Exception as ex:
        raise Exception(ex)
    finally:
        print("### Cierro Conexion ###")
        conn.close()