from flask import jsonify
import json
from bson import ObjectId

def errorResponse(errorDescription,statusCode):
    return jsonify({'success' : False , 'error' : {'statusCode': statusCode ,  'description' : errorDescription} , 'statusCode' : statusCode , 'result' : None})

def successResponse(data,statusCode):
    return jsonify({'success' : True , 'error' : None, 'statusCode' : statusCode , 'result' : data})



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)