import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
import pdb
from json_encoder import JSONEncoder
# 1
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps


template = Flask(__name__)
#
template.config['DEBUG'] = True
# 2
mongo = MongoClient('localhost', 27017)

# 3
template.db = mongo.Test


class User(Resource):

    def post(self):
        
        name = request.args.get('name')

        new_user = request.json

        users_collection = template.db.users
        pdb.set_trace() 
        result = users_collection.insert_one(new_user)

        

        user = users_collection.find_one({'name': name})

        
        return (user,200,None)

    def get(self):

        # 1 Get Url params
        name = request.args.get('name')

        # 2 Our users users collection
        users_collection = template.db.users

        # 3 Find document in users collection
        result = users_collection.find_one(
            {'name': name}
        )

        # 4 Convert result to json from python dict
        json_result = JSONEncoder().encode(result)
        pdb.set_trace()
        # 5 Return json as part of the response body
        return (json_result, 200, None)

    def patch(self):

        users_collection = template.db.users

        name = request.args.get('name')
        new_name = request.args.get('new_name')
        age = request.args.get('age', type=int)
        location = request.args.get('location')

        user = users_collection.find_one_and_update(
            {'name': name},
            {'$set':
                    {
                        'name': new_name,
                        'age': age,
                        'location': location
                    }
            })

        if user == None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return (user, 200, None)

api = Api(template)
api.add_resource(User, '/users')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    template.config['TRAP_BAD_REQUEST_ERRORS'] = True
    template.run(debug=True, port = 8080)
