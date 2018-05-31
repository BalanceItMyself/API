"""
Date Created: 01-06-2018
@author: Vijayasai.S
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
from SampleUsers import users


class User(Resource):

    def get(self, name):
        for user in users:
            user_name = user.get("name", None)
            if user_name:
                if user_name == name:
                    return user, 200
        return "User {} not found".format(name), 404
    
    def post(self, name):
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

    def put(self, name):
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

    def delete(self, name):
        global users
        users = [user for user in users if user.get("name", None) != name]
        return "User {} is deleted".format(name), 200


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(User, "/user/<string:name>")
    app.run(debug=True)
