from datetime import datetime
import json
import logging


from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema

from app.udaconnect import location_pb2 as location__pb2
from google.protobuf.json_format import MessageToJson

from app.udaconnect.services import  LocationService, LocationEventService
from flask import request, jsonify, make_response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
# from typing import Optional, List

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

@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self) -> Location:
        locationevent=request.get_json()
        logger.info(struct_message('Location sent from locations-event stream', 
        locationevent=locationevent))
        LocationEventService.producelocationevent(locationevent)
        return  make_response(jsonify("OK"))

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    def get(self, location_id):

        if location_id.isnumeric():
            location: location__pb2.LocationMessage = LocationService.retrieve(location_id)
            locationASJSON=json.loads(MessageToJson(location, preserving_proto_field_name=True))
            if locationASJSON['id'] == -1 :
                logger.error(struct_message('Location for Location ID not found', locationid=location_id))
                response = make_response(jsonify({"Error": "Oups location not found"}), 404,)
                return response
            
            logger.info(struct_message('Location received from location-grpc', 
            personid=locationASJSON['person_id'] , 
            latitude=locationASJSON['latitude'] , 
            longitude=locationASJSON['longitude'], createdat=locationASJSON['creation_time']))

            return locationASJSON
        else:
            logger.error(struct_message('Unauthorized Numerical value is required'))
            return make_response(jsonify({"Unauthorized": "Numerical value as parameter is required"}), 401,)
        

