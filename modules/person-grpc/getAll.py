import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5007")
stub = person_pb2_grpc.PersonServiceStub(channel)

response = stub.GetAll(person_pb2.EmptyMessage())
print(response)