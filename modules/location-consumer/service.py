import json
import faust
import os
import logging

# import database from session 
from models import session, Location
from geoalchemy2.functions import ST_AsText, ST_Point

# grpc 
import grpc
import person_pb2
import person_pb2_grpc

# grpc variables
GRPC_HOST = os.environ["GRPC_HOST"]
GRPC_PORT = os.environ["GRPC_PORT"]
KAFKA_HOST= os.environ["KAFKA_HOST"]
KAFKA_PORT= os.environ["KAFKA_PORT"]

# structured data for logs 
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

struct_message = StructuredMessage

# this model describes how message values are serialized
# in the Kafka "location-events" topic.
class LocationEvent(faust.Record, validation=True):
    latitude: str
    longitude: str
    person_id: int
    id: int
    creation_time: str

# app = faust.App(
#     'location-app', 
#     broker='kafka://kafka:9092')

app = faust.App(
    'location-app', 
    broker=f"kafka://{KAFKA_HOST}:{KAFKA_PORT}")

locations_kafka_topic = app.topic('location-events', value_type=LocationEvent)

@app.agent(locations_kafka_topic)
async def process(locationevents):
    async for locationevent in locationevents:
        app.logger.info(struct_message('Location received from locations-event stream', 
        personid=locationevent.person_id, 
        latitude=locationevent.latitude, 
        longitude=locationevent.longitude, 
        createdat=locationevent.creation_time))
        createlocation(locationevent)


def createlocation(locationevent):
        # TODO : gRPC call to person-grpc : function exists
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        person = stub.Get(person_pb2.PersonIdMessage(id=int(locationevent.person_id)))
        if person.id > 0:
            new_location = Location()
            new_location.person_id = locationevent.person_id
            new_location.creation_time = locationevent.creation_time
            new_location.coordinate = ST_Point(locationevent.latitude, locationevent.person_id)
            try:
                session.add(new_location)
                session.commit()
                app.logger.info(struct_message('Location persisted in LocationDB', 
                personid=locationevent.person_id, 
                latitude=locationevent.latitude, 
                longitude=locationevent.longitude, 
                createdat=locationevent.creation_time))
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else: 
            app.logger.error(struct_message('Person for LocationEvent person ID not found', 
            personid=locationevent.person_id))
        


if __name__ == '__main__':
    FORMAT = '%(levelname)s:%(name)s:%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')
    app.main()