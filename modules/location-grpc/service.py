import time
import sys
import json

from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

import logging

# import database from session 
from models import session,  Location

# structured data for logs 
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

struct_message = StructuredMessage

# setting the logger 
log = logging.getLogger()


# TODO : change all prints into logs

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):

        
        log.info(struct_message('Location ID in Request', locationid=request.id))

        try:
            location, coord_text = (
                session.query(Location, Location.coordinate.ST_AsText())
                .filter(Location.id == request.id)
                .one()
            )
        except:
            log.error(struct_message('Location is not found in LocationDB'))
            session.rollback()
            raise
        finally:
            session.close()

        # # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text

        locationresponse = location_pb2.LocationMessage(
            id = location.id,
            person_id = location.person_id,
            longitude = location.longitude,
            latitude = location.latitude,
            creation_time = location.creation_time.strftime("%m/%d/%Y, %H:%M:%S")
        )

        log.info(struct_message('Location received from LocationDB', 
        personid=locationresponse.person_id , 
        latitude=locationresponse.latitude , 
        longitude=locationresponse.longitude, createdat=locationresponse.creation_time))

        return locationresponse

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    log.info(struct_message("Server starting on port 5005..."))
    server.add_insecure_port('[::]:5005')
    server.start()
    try:
      while True:
        time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    FORMAT = '%(levelname)s:%(name)s:%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')
    serve()


