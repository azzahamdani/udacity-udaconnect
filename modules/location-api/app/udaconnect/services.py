import logging
# from datetime import datetime, timedelta
from json import dumps
from typing import Dict, List

from app.udaconnect.schemas import  LocationSchema

import os
# from kafka import KafkaProducer
from confluent_kafka import Producer

import grpc
from app.udaconnect import location_pb2 as location__pb2
from app.udaconnect import location_pb2_grpc

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

# kafka variables 
topic_name = os.environ["TOPIC_NAME"]
kafka_server = os.environ["KAFKA_SERVER"]

# grpc variables
GRPC_HOST = os.environ["GRPC_HOST"]
GRPC_PORT = os.environ["GRPC_PORT"]

class LocationEventService: 
    def producelocationevent(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        # TODO : produce a message using kafka python
        # producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: dumps(v).encode('utf-8'))
        # producer.send(topic_name, dumps(location))
        # producer.flush()
        producer = Producer({'bootstrap.servers': kafka_server})
        producer.produce(topic_name, value=dumps(location))
        producer.flush()

class LocationService:
    @staticmethod
    def retrieve(location_id) -> location__pb2.LocationMessage:
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        stub = location_pb2_grpc.LocationServiceStub(channel)
        location = stub.Get(location__pb2.LocationIdMessage(id=int(location_id)))
        return location


