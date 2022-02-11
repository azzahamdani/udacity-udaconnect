import time
import sys
import json
from concurrent import futures
import traceback
sys.tracebacklimit = 0

import logging

import grpc
import person_pb2
import person_pb2_grpc

# import database from session 
from models import session, Person

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

class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    
    def Get(self, request, context):

        log.info(struct_message('Person ID in Request', personid=request.id))

        person = session.query(Person).get(request.id)
        if person is None:
            log.error(struct_message('Person for Person ID not found', personid=request.id))
            result = person_pb2.PersonMessage(
            id=-1,
            first_name="",
            last_name="",
            company_name="",
        )
        else :
            log.info( struct_message('Person received from PersonDB', 
            id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            company_name=person.company_name) )

            result = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name,
            )
        return result
    
    def GetAll(self, request, context):

        persons = session.query(Person).all()
        result = person_pb2.PersonListMessage()
        
        for person in persons :
            current_person = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name,
            )
            result.persons.extend([current_person])

        return result

    def Create(self, request, context):

        log.info(struct_message('Person received from Request',
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name) )

        new_person = Person()
        new_person.first_name = request.first_name
        new_person.last_name = request.last_name
        new_person.company_name = request.company_name

        try:
            session.add(new_person)
            session.commit() 
        except Exception as e:
            log.error(struct_message('Person is not persisted in PersonDB'))
            session.rollback()
            raise Exception(traceback.print_stack())
        finally:
            session.close()

        log.info(struct_message('Person persisted in PersonDB',
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name) )

        request_person = person_pb2.PersonMessage(
            id=request.id,
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name,
        )
        return request_person
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)
    log.info("Server starting on port 5005...")
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
