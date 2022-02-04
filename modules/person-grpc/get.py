import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5007")
stub = person_pb2_grpc.PersonServiceStub(channel)

# nominal scenario 
response = stub.Get(person_pb2.PersonIdMessage(id=6))
print(response)

# error scenario
# response = stub.Get(person_pb2.PersonIdMessage(id=2))
# print(response)