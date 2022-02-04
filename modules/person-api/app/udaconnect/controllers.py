from datetime import datetime
import json

from app.udaconnect.models import Person
# from app.udaconnect.models import Connection, Location
# from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from app.udaconnect.schemas import PersonSchema


from app.udaconnect import person_pb2 as person__pb2
from google.protobuf.json_format import MessageToJson, MessageToDict

# from app.udaconnect.services import ConnectionService, LocationService, PersonService
from app.udaconnect.services import PersonService
from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self): # -> Person
        payload = request.get_json()
        new_person: person__pb2.PersonMessage = PersonService.create(payload)
        return jsonify(json.loads(MessageToJson(new_person)))

    # @responds(schema=PersonSchema, many=True)
    def get(self): # -> List[Person]
        persons: person__pb2.PersonListMessage = PersonService.retrieve_all()
        return jsonify(json.loads(MessageToJson(persons)))


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    # @responds(schema=PersonSchema)
    def get(self, person_id): # -> Person
        if person_id.isnumeric():
            person: person__pb2.PersonMessage = PersonService.retrieve(person_id)
            # TODO : send {"Error: Oups person not found"} 
            return jsonify(json.loads(MessageToJson(person)))
        else:
            return jsonify({"Unauthorized": "Numerical value as parameter is required"})


