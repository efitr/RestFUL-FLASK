import json
from flask import Flask, request

template = Flask(__name__)

@template.route('/person')
def person_route():
    person = {"name": "Eliel", 'age': 23}
    json_person = json.dumps(person)
    return (json_person, 200, None)

if '__name__' = '__main__':
    template.run()
    template.config("DEBUG") = True