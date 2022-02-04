import time
import sys
import json
from concurrent import futures

import logging

import grpc
import person_pb2
import person_pb2_grpc

# import database from session 
from models import session, Person


# setting the logger 
log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    
    def Get(self, request, context):

        person = session.query(Person).get(request.id)
        if person is None:
            log.info("None")
            result = person_pb2.PersonMessage(
            id=-1,
            first_name="",
            last_name="",
            company_name="",
        )
        else :
            log.info("Received Person" + str(person) )
            result = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name,
            )
        return result
    
    def GetAll(self, request, context):

        persons = session.query(Person).all()
        log.info("Received a message!: " + str(persons))

        result = person_pb2.PersonListMessage()
        for person in persons :
            current_person = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name,
            )
            result.personmessages.extend([current_person])
        return result

    def Create(self, request, context):

        new_person = Person()
        new_person.first_name = request.first_name
        new_person.last_name = request.last_name
        new_person.company_name = request.company_name

        try:
            session.add(new_person)
            session.commit() 
        except:
            session.rollback()
            raise
        finally:
            session.close()

        
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
    logging.basicConfig()
    serve()
