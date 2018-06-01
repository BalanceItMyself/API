"""
Date Created: 02-06-2018
Project: BalanceIt
@author: Vijayasai.S
"""

from flask import Flask
from flask_restful import Api
from Users.Users import Users


def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Users, "/user/<string:name>")
    app.run(host="0.0.0.0", threaded=True)


if __name__ == "__main__":
    main()


