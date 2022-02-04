import time
import sys

from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

import logging

# import database from session 
from models import session, Person, Location

# setting the logger 
log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# TODO : change all prints into logs

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):

        log.info("Received a message!: " + str(request))
    
        # try to query for a person in the database to test ORM config
        # person = session.query(Person).get(5)
        # log.info("Received Person: " + str(person.id) + person.first_name)

        location, coord_text = (
            session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == request.id)
            .one()
        )
        

        # # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text

        
        locationresponse = location_pb2.LocationMessage(
            id = location.id,
            person_id = location.person_id,
            longitude = location.longitude,
            latitude = location.latitude,
            created_at = location.creation_time.strftime("%m/%d/%Y, %H:%M:%S")
        )

        log.info("Received Location: " + str(locationresponse))

        # locationresponse = location_pb2.LocationMessage(
        #     id = 33,
        #     person_id = 4,
        #     longitude = "14",
        #     latitude = "55",
        #     created_at = "2020-03-02"
        # )

        return locationresponse

    def Create(self, request, context):
        print("Received a message!")  

        location_value = {
            "id": request.id,
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "created_at": request.created_at
        }
        print(location_value)

        # TODO : reach out to database and create the location

        return location_pb2.LocationMessage(**location_value)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    log.info("Server starting on port 5005...")
    server.add_insecure_port('[::]:5005')
    server.start()
    try:
      while True:
        time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()


