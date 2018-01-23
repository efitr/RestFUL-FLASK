import json
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from pymongo import ReturnDocument
import pdb
# 1
import bcrypt
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

from json_encoder import JSONEncoder
app = Flask(__name__)
api = Api(app)

# 2
#mongo = MongoClient('localhost', 27017)
mongo = MongoClient('mongodb://eft:nadanada@ds125716.mlab.com:25716/trip_planner_production')
app.db = mongo.trip_planner_production
# 3
user_collection = app.db.users
app.bcrypt_rounds = 12


def _validate_auth(email, password):
    # pdb.set_trace()
    user_collection = app.db.users
    user = user_collection.find_one({'email': email})

    if user is None:
        return False
    else:
        # check if the hash we generate based on auth matches stored hash
        g.setdefault('user', user)
        return bcrypt.checkpw(
            password.encode('utf-8'), user['password'].encode('utf-8'))


def authenticated_request(func):
    """Handle HTTP request methods that require basic auth."""
    def wrapper(*args, **kwargs):
        auth = request.authorization

        if not auth or not _validate_auth(auth.username, auth.password):
            return ({'error': 'Basic Auth Required.'}, 401, None)

        return func(*args, **kwargs)

    return wrapper

class User(Resource):

    def post(self):

        user_email = request.json['email']
        user_password = request.json['password']

        hashed_password = bcrypt.hashpw(
            user_password.encode('utf-8'), bcrypt.gensalt(app.bcrypt_rounds)
        ).decode()

        result = user_collection.insert_one(
            {"email": user_email, "password": hashed_password, "trips": []}
        )
        posted_user = user_collection.find_one(
            {'_id': ObjectId(result.inserted_id)}
        )

        return (posted_user, 201, None)

    @authenticated_request
    def get(self):

        username = request.authorization.username

        user = user_collection.find_one({'email': username})

        return (user, 200, None)

    @authenticated_request
    def put(self):

        username = request.authorization.username

        result = users_collection.find_one_and_replace({'email': username}), user

        return result

    @authenticated_request
    def patch(self):

        updated_info = request.json
        email = request.args.get('email')

        result = user_collection.find_one_and_update(
            {'email': email},
            {'$set': updated_info}
        )

        return result

    @authenticated_request
    def delete(self):

        email = request.authorization.username

        result = user_collection.find_one_and_delete(
            {'email': email}
        )

        return result

class Trip(Resource):

    @authenticated_request
    def get(self):

        email = request.args.get('email')

        user = user_collection.find_one({'email': email})

        return user['trips']

    @authenticated_request
    def post(self):
        trip = request.json
        email = request.args.get('email')

        result = user_collection.find_one_and_update(
            {'email': email},
            {'$push': {'trips': trip}}
        )

        return (result, 201, None)

    @authenticated_request
    def put(self):

        trip = request.json
        email = request.args.get('email')
        trip_index = request.args.get('trip_index')

        result = user_collection.find_one_and_update(
            {'email': email},
            {'$set': {'trips.' + trip_index: trip}}
        )

        return result

    @authenticated_request
    def patch(self):

        self.put()

    def delete(self):

        email = request.args.get('email')
        trip_name = request.args.get('trip_name')

        result = user_collection.find_one_and_update(
            {'email': email},
            {'$pull': {'trips': {'name': trip_name}}}
        )

        return result


api.add_resource(User, '/users')

api.add_resource(Trip, '/users/trips')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)