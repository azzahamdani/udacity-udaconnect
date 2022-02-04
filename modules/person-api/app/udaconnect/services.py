import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Person
# from app.udaconnect.models import Connection, Location, Person
# from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from app.udaconnect.schemas import PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

import grpc
from app.udaconnect import person_pb2 as person__pb2
from app.udaconnect import person_pb2_grpc

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

# grpc variables
GRPC_HOST = os.environ["GRPC_HOST"]
GRPC_PORT = os.environ["GRPC_PORT"]

class PersonService:
    @staticmethod
    def create(person: Dict) -> person__pb2.PersonMessage:
        validation_results: Dict = PersonSchema().validate(person)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)

        try: 
            response = stub.Create(person__pb2.PersonMessage(id=person["id"],
                        first_name=person["first_name"],
                        last_name=person["last_name"],
                        company_name=person["company_name"],))
            return response
        except:
            return person__pb2.PersonMessage(id=-1,
                        first_name="",
                        last_name="",
                        company_name="",)

    @staticmethod
    def retrieve(person_id: int) -> person__pb2.PersonMessage:
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        person = stub.Get(person__pb2.PersonIdMessage(id=int(person_id)))
        return person

    @staticmethod
    def retrieve_all() -> person__pb2.PersonListMessage:
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        personlist = stub.GetAll(person__pb2.EmptyMessage())
        return personlist
