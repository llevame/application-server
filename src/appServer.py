from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class ApplicationServer(Resource):
    def get(self):
        return 'Application Server api'

class HomePage(Resource):
    def get(self):
        return 'Homepage'

api.add_resource(HomePage, '/')
api.add_resource(ApplicationServer, '/api')

if __name__ == "__main__":
    app.run(host = 'localhost')

