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
        # locations: List = db.session.query(Location).filter(
        #     Location.person_id == person_id
        # ).filter(Location.creation_time < end_date).filter(
        #     Location.creation_time >= start_date
        # ).all()

        # # Prepare arguments for queries
        # data = []
        # for location in locations:
        #     data.append(
        #         {
        #             "person_id": person_id,
        #             "longitude": location.longitude,
        #             "latitude": location.latitude,
        #             "meters": meters,
        #             "start_date": start_date.strftime("%Y-%m-%d"),
        #             "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
        #         }
        #     )

        # logger.info(struct_message('Loactions', locations=str(locations)))
        # logger.info(struct_message('dataforquery', locations=data))

        # TODO : location - grpc call
        # # Cache all users in memory for quick lookup 
        
        # person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}
        channel = grpc.insecure_channel(f"{PERSON_GRPC_HOST}:{PERSON_GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        personlist = stub.GetAll(person__pb2.EmptyMessage())
        person_map: Dict[str, Person] = {person.id: person for person in personlist.persons}

        # TODO : person - grpc call
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

        # query = text(
        #     """
        # SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        # FROM    location
        # WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        # AND     person_id != :person_id
        # AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        # AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        # """
        # )
        # # result: List[Connection] = []
        # result: List(Connection) = []
        # for line in tuple(data):
        #     for (
        #         exposed_person_id,
        #         location_id,
        #         exposed_lat,
        #         exposed_long,
        #         exposed_time,
        #     ) in db.engine.execute(query, **line):
        #         location = Location(
        #             id=location_id,
        #             person_id=exposed_person_id,
        #             creation_time=exposed_time,
        #         )
        #         location.set_wkt_with_coords(exposed_lat, exposed_long)
        #         result.append(location)

        #         # result.append(
        #         #     Connection(
        #         #         person=person_map[exposed_person_id], location=location,
        #         #     )
        #         # )
        # logger.info(struct_message('Loactions Number', number=len(result)))
        # logger.info(struct_message('Loaction result', result=str(result)))
        # return result
        return result


# class LocationService:
#     @staticmethod
#     def retrieve(location_id) -> Location:
#         location, coord_text = (
#             db.session.query(Location, Location.coordinate.ST_AsText())
#             .filter(Location.id == location_id)
#             .one()
#         )

#         # Rely on database to return text form of point to reduce overhead of conversion in app code
#         location.wkt_shape = coord_text
#         return location

#     @staticmethod
#     def create(location: Dict) -> Location:
#         validation_results: Dict = LocationSchema().validate(location)
#         if validation_results:
#             logger.warning(f"Unexpected data format in payload: {validation_results}")
#             raise Exception(f"Invalid payload: {validation_results}")

#         new_location = Location()
#         new_location.person_id = location["person_id"]
#         new_location.creation_time = location["creation_time"]
#         new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
#         db.session.add(new_location)
#         db.session.commit()

#         return new_location


# class PersonService:
#     @staticmethod
#     def create(person: Dict) -> Person:
#         new_person = Person()
#         new_person.first_name = person["first_name"]
#         new_person.last_name = person["last_name"]
#         new_person.company_name = person["company_name"]

#         db.session.add(new_person)
#         db.session.commit()

#         return new_person

#     @staticmethod
#     def retrieve(person_id: int) -> Person:
#         person = db.session.query(Person).get(person_id)
#         return person

#     @staticmethod
#     def retrieve_all() -> List[Person]:
#         return db.session.query(Person).all()
