"""
Date Created: 02-06-2018
Project: BalanceIt
@author: Vijayasai.S
"""

from flask_restful import Resource, reqparse


class Users(Resource):

    @staticmethod
    def get(name):
        for user in users:
            user_name = user.get("name", None)
            if user_name:
                if user_name == name:
                    return user, 200
        return "User {} not found".format(name), 404

    @staticmethod
    def post(name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")

        args = parser.parse_args()

        for user in users:
            user_name = user.get("name", None)
            if user_name:
                if user_name == name:
                    return "User with name {} already exists".format(name), 400

        user = {}
        user.update({
            "name": name,
            "age": args.get("age", None),
            "occupation": args.get("occupation", None)
        })
        users.append(user)
        return user, 201

    @staticmethod
    def put(name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            user_name = user.get("name", None)
            if user_name:
                if user_name == name:
                    age = args.get("age", None)
                    occupation = args.get("occupation", None)
                    user.update({
                        "age": age,
                        "occupation": occupation
                    })
                    return user, 200
        user = {}
        user.update({
            "name": name,
            "age": args.get("age", None),
            "occupation": args.get("occupation", None)
        })
        return user, 201

    @staticmethod
    def delete(name):
        global users
        users = [user for user in users if user.get("name", None) != name]
        return "User {} is deleted".format(name), 200
