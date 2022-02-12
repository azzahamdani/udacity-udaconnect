import grpc
import json
import location_pb2
import location_pb2_grpc
from google.protobuf.json_format import MessageToJson

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)


locationrequest= location_pb2.LocationRequestMessage(
    person_id=6,
    start_date='2020-01-01',
    end_date='2020-12-30',
    meters=5,
)
 
# response = stub.GetLocationPersonId(locationrequest)
# locations = json.loads(MessageToJson(response, preserving_proto_field_name=True) ) 
# print(locations['locations'])

response2= stub.GetLocationPersonConnections(locationrequest)
locations2 = json.loads(MessageToJson(response2, preserving_proto_field_name=True) ) 
print(locations2['locations'])