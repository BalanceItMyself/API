"""
Date Created: 02-06-2018
Project: BalanceIt
@author: Vijayasai.S
"""

import hashlib
from passlib.hash import sha256_crypt
from flask_restful import Resource, reqparse
from DatabaseManager.PostgresManager import PostgresManager

pg_manager = PostgresManager()
pg_connection = pg_manager.create_connection()
pg_cursor_read = pg_manager.get_cursor(connection=pg_connection, read_only=True)
pg_cursor_write = pg_manager.get_cursor(connection=pg_connection, read_only=False)


def create_unique_hash(unique_string):
    return hashlib.md5(unique_string.strip().encode("utf-8")).hexdigest()


class Users(Resource):

    @staticmethod
    def get(name):
        query = "select * from cloud.users where user_name='{}'".format(name)
        users = pg_manager.query_output(cursor=pg_cursor_read, query=query)
        if users:
            user = users[0] if len(users) > 0 else None
            if user:
                return user, 200
        return "User {} not found".format(name), 404

    @staticmethod
    def post(name):
        parser = reqparse.RequestParser()
        parser.add_argument("mail")
        parser.add_argument("password")

        args = parser.parse_args()

        query = "select * from cloud.users where user_name='{}'".format(name)
        users = pg_manager.query_output(cursor=pg_cursor_read, query=query)
        if users:
            user = users[0] if len(users) > 0 else None
            if user:
                return "User with name {} already exists".format(name), 400

        user = {}
        user.update({
            "user_name": name,
            "user_mail": args.get("mail", None),
            "user_password": args.get("password", None)
        })

        unique_string = "{}_{}".format(user.get("user_name", None), user.get("user_mail", None))
        hash_id = create_unique_hash(unique_string=unique_string)

        encrypted_password = sha256_crypt.hash(user.get("user_password", None))

        user.update({
            "user_id": hash_id,
            "user_password": encrypted_password
        })

        query = "insert into cloud.users (user_id, user_name, user_mail, user_password) " \
                "values('{}', '{}', '{}', '{}')".format(user.get("user_id"), user.get("user_name"),
                                                        user.get("user_mail"), user.get("user_password"))
        pg_manager.query_insert(connection=pg_connection, cursor=pg_cursor_write, query=query)
        return user, 201

    @staticmethod
    def put(name):
        parser = reqparse.RequestParser()
        parser.add_argument("mail")
        parser.add_argument("password")

        args = parser.parse_args()

        query = "select * from cloud.users where user_name='{}'".format(name)
        users = pg_manager.query_output(cursor=pg_cursor_read, query=query)
        if users:
            user = users[0] if len(users) > 0 else None
            if user:
                mail = args.get("mail", None)
                password = args.get("password", None)

                unique_string = "{}_{}".format(name, mail)
                hash_id = create_unique_hash(unique_string=unique_string)

                encrypted_password = sha256_crypt.hash(password)

                query = "update cloud.users set user_id='{}', user_mail='{}', " \
                        "user_password='{}' where user_name='{}'".format(hash_id, mail, encrypted_password, name)
                pg_manager.query_insert(connection=pg_connection, cursor=pg_cursor_write, query=query)

                return user, 200

        user = {}
        user.update({
            "user_name": name,
            "user_mail": args.get("mail", None),
            "user_password": args.get("password", None)
        })

        unique_string = "{}_{}".format(user.get("user_name", None), user.get("user_mail", None))
        hash_id = create_unique_hash(unique_string=unique_string)

        encrypted_password = sha256_crypt.hash(password)

        user.update({
            "user_id": hash_id,
            "user_password": encrypted_password
        })

        query = "insert into cloud.users (user_id, user_name, user_mail, user_password) " \
                "values('{}', '{}', '{}', '{}')".format(user.get("user_id"), user.get("user_name"),
                                                        user.get("user_mail"), user.get("user_password"))
        pg_manager.query_insert(connection=pg_connection, cursor=pg_cursor_write, query=query)
        return user, 201

    @staticmethod
    def delete(name):
        query = "delete from cloud.users where user_name='{}'".format(name)
        pg_manager.query_insert(connection=pg_connection, cursor=pg_cursor_write, query=query)
        return "User {} is deleted".format(name), 200
