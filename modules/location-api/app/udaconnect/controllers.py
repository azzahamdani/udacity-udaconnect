from datetime import datetime
import json

from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema

from app.udaconnect import location_pb2 as location__pb2
from google.protobuf.json_format import MessageToJson

from app.udaconnect.services import  LocationService, LocationEventService
from flask import request, jsonify, make_response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"
api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# TODO: This needs better exception handling

@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        LocationEventService.producelocationevent(request.get_json())
        return  make_response(jsonify("OK"))

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    def get(self, location_id):
        location: location__pb2.LocationMessage = LocationService.retrieve(location_id)
        return json.loads(MessageToJson(location))


