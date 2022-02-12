import json
import logging

from app.udaconnect.schemas import PersonSchema
from app.udaconnect import person_pb2 as person__pb2
from google.protobuf.json_format import MessageToJson

from app.udaconnect.services import PersonService
from flask import request, jsonify, make_response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

logger = logging.getLogger()

# structured data for logs 
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

struct_message = StructuredMessage

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    def post(self):
        payload = request.get_json()
        new_person: person__pb2.PersonMessage = PersonService.create(payload)
        newpersonAsJSON=json.loads(MessageToJson(new_person, preserving_proto_field_name=True))
        if newpersonAsJSON['id'] == -1:
            logger.error(struct_message('Person Was not persisted in PersonDB', id=newpersonAsJSON['id']))
            return make_response(jsonify({"Error": "Person Was not persisted in database"}), 500,)
        
        logger.info(struct_message('Person persisted in PersonDB',
            first_name=newpersonAsJSON['first_name'],
            last_name=newpersonAsJSON['last_name'],
            company_name=newpersonAsJSON['company_name']) )

        return newpersonAsJSON

    def get(self): 
        personlistmessage: person__pb2.PersonListMessage = PersonService.retrieve_all()
        personlistmessageAsJSON=json.loads(MessageToJson(personlistmessage, preserving_proto_field_name=True))
        logger.info(struct_message('Persons received from person-grpc server', persons=personlistmessageAsJSON))
        return personlistmessageAsJSON['persons']  


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    def get(self, person_id):
        if person_id.isnumeric():
            person: person__pb2.PersonMessage = PersonService.retrieve(person_id)
            personAsJSON=json.loads(MessageToJson(person, preserving_proto_field_name=True))
            if personAsJSON['id'] == -1 :
                logger.error(struct_message('Person for Person ID not found', personid=person_id))
                response = make_response(jsonify({"Error": "Oups person not found"}), 404,)
                return response
            
            logger.info(struct_message('Person receivd from person-grpc',
            first_name=personAsJSON['first_name'],
            last_name=personAsJSON['last_name'],
            company_name=personAsJSON['company_name']) )

            return personAsJSON
        else:
            logger.error(struct_message('Unauthorized Numerical value is required'))
            return make_response(jsonify({"Unauthorized": "Numerical value as parameter is required"}), 401,)
            


