import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app import struct_message
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

import grpc
from app.udaconnect import location_pb2 as location__pb2
from app.udaconnect import location_pb2_grpc
from app.udaconnect import person_pb2 as person__pb2
from app.udaconnect import person_pb2_grpc


logger = logging.getLogger("udaconnect-api")

# grpc variables
LOCATION_GRPC_HOST = os.environ["LOCATION_GRPC_HOST"]
LOCATION_GRPC_PORT = os.environ["LOCATION_GRPC_PORT"]
PERSON_GRPC_HOST = os.environ["PERSON_GRPC_HOST"]
PERSON_GRPC_PORT = os.environ["PERSON_GRPC_PORT"]

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:

        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """

        # person - grpc call
        channel = grpc.insecure_channel(f"{PERSON_GRPC_HOST}:{PERSON_GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        personlist = stub.GetAll(person__pb2.EmptyMessage())
        person_map: Dict[str, Person] = {person.id: person for person in personlist.persons}

        # location - grpc call
        channel = grpc.insecure_channel(f"{LOCATION_GRPC_HOST}:{LOCATION_GRPC_PORT}")
        stub = location_pb2_grpc.LocationServiceStub(channel)
        
        locationrequest= location__pb2.LocationRequestMessage(
            person_id=int(person_id),
            start_date= start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            meters=int(meters),
        )
        
        locationconnections = stub.GetLocationPersonConnections(locationrequest)

        # construct response
        result: List[Connection] = []
        for locationconn in locationconnections.locations:
            location = Location(
                id=locationconn.id,
                person_id=locationconn.person_id,
                creation_time=datetime.strptime(locationconn.creation_time,'%Y-%m-%d' )
            )
            location.set_wkt_with_coords(locationconn.latitude, locationconn.longitude)
            result.append(
                Connection(
                    person=person_map[locationconn.person_id], location=location,
                )
            )
        
        logging.info(result)
        return result

