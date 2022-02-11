import json
import grpc
import person_pb2
import person_pb2_grpc
from google.protobuf.json_format import MessageToJson

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5007")
stub = person_pb2_grpc.PersonServiceStub(channel)

response = stub.GetAll(person_pb2.EmptyMessage())
persons = json.loads(MessageToJson(response, preserving_proto_field_name=True) ) 

print ( persons['persons'])