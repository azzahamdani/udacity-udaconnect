import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5007")
stub = person_pb2_grpc.PersonServiceStub(channel)

try: 
    response = stub.Create(person_pb2.PersonMessage(id=2,
                first_name="hedi",
                last_name="elabed",
                company_name="Mbition",))
    print(response)
except:
    print('person could not be accepted in database')