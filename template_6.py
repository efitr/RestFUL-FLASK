import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import ReturnDocument
import pdb
import bcrypt
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps
from until import JSONEncoder

app = Flask(__name__)
api = Api(app)

mongo = MongoClient('localhost', 27017)

app.bcrypt_rounds = 12
app.db = mongo.local

class Meme(Resource):

    def post(self):
        meme_collection = app.db.memes
        new_meme = request.json
        result = meme_collection.insert_one(new_meme)
        meme = meme_collection.find_one({'_id': result.inserted_id})

        if result is not None:
            return(meme, 201, {"Content-Type": "application/json", "Meme": "Meme 0"})
        else:
            return (None, 400, None)

    def get(self):
        image = request.args.get('image')
        meme_collection = app.db.memes
        result = meme_collection.find_one(
            {'image': image}
        )

        if result is not None:
            return (result, 200, None)
        else:
            return (None, 404, None)

    def put(self):
        image = request.args.get('image')
        meme_collection = app.db.memes
        new_meme = request.json
        result = meme_collection.find_one_and_replace({'email': email}, new_meme, return_document=ReturnDocument.AFTER)

        if result is not None:
            return (result, 200, {'Content-Type': 'application/json', 'meme': 'meme'})
        else:
            return (None, 404, None)

    def patch(self):
        image = request.args.get('image')
        meme_collection = app.db.memes
        new_meme = request.json
        set_values = {}
        if 'image' in new_meme:
            set_values['image'] = new_meme['image']
        if 'image_color' in new_meme:
            set_values['image_color'] = new_meme['image_color']
        
        mongo_set = {'$set': set_values}

        result = meme_collection.find_one_and_update(
            {'image': image},
            mongo_set,
            return_document=ReturnDocument.AFTER
        )

        if result is not None:
            return(result, 200, {'Content-Type': 'application/json', 'meme': 'image_color'})
        else:
            return (None, 404, None)

    def delete(self):
        meme = request.args.get('meme')
        result = meme_collection.find_one_and_delete(
            {'meme': meme}
        )

        return result 


if '__name__' = '__main__':
    app.run()
    app.config("DEBUG") = True