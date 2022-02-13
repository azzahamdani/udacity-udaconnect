import time
# import sys
import json

from concurrent import futures
from datetime import datetime, timedelta
from sqlalchemy.sql import text

import grpc
import location_pb2
import location_pb2_grpc
from google.protobuf.json_format import MessageToJson

import logging

# import database from session 
from models import session,  Location, db

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
    
    def GetLocationPersonConnections(self, request, context):

        log.info(struct_message('Request', id=request.person_id , 
            start_date=request.start_date, 
            end_date=request.end_date , 
            meters=request.meters))
        
        start_date_datetime= datetime.strptime(request.start_date,'%Y-%m-%d' )
        end_date_datetime= datetime.strptime(request.end_date,'%Y-%m-%d' )

        locations = session.query(Location).filter(
            Location.person_id == request.person_id
        ).filter(Location.creation_time < end_date_datetime).filter(
            Location.creation_time >= start_date_datetime
        ).all()
        
        log.info(struct_message('Locations for PersonID from LocationDB', locations=str(locations)))

        data = []
        for location in locations:
            data.append(
                {
                    "person_id": location.person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": request.meters,
                    "start_date": request.start_date,
                    "end_date": (end_date_datetime + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )
      
        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        locationsconnections = location_pb2.LocationsConnections()

        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                locationconnection=location_pb2.LocationMessage(
                    id=location.person_id,
                    person_id=location.person_id,
                    longitude=location.longitude,
                    latitude=location.latitude,
                    creation_time=location.creation_time.strftime('%Y-%m-%d')
                )
                locationsconnections.locations.extend([locationconnection])
                
        log.info(struct_message('Location Connections Received from LocationDB', locations=json.loads(MessageToJson(locationsconnections,preserving_proto_field_name=True ))))
        return locationsconnections


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


