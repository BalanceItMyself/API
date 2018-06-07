"""
Date Created: 02-06-2018
Project: BalanceIt
@author: Vijayasai.S
"""


import psycopg2
import psycopg2.extras
from .Configuration import Configuration

config = Configuration.get_conf()


class PostgresManager:

    def __init__(self):
        pass

    @staticmethod
    def create_connection():
        connection = psycopg2.connect(host=config.postgresdb_host, port=config.postgresdb_port,
                                user=config.postgresdb_username, password=config.postgresdb_password,
                                dbname=config.postgresdb_database)
        return connection

    @staticmethod
    def get_cursor(connection, read_only=False):
        if read_only:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cursor = connection.cursor()
        return cursor

    @staticmethod
    def query_output(cursor, query):
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    @staticmethod
    def query_insert(connection, cursor, query):
        cursor.execute(query)
        connection.commit()
        return





