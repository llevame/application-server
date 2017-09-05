from flask import Flask
from flask_restful import Resource, Api

from resources.users import Users
from resources.users import UsersIds

app = Flask(__name__)
api = Api(app)

prefix = "/api/v1"

api.add_resource(Users, '{}/users'.format(prefix))
api.add_resource(UsersIds, '{}/users/<int:userId>'.format(prefix))

if __name__ == "__main__":
    app.run(host = 'localhost')

