import psycopg2
from psycopg2.extras import RealDictCursor  # para que fetch devuelva diccionarios

def get_connection():
    return psycopg2.connect(
        dbname="tia_dataset",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )