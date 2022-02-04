## Generating gRPC files
`pip install grpcio-tools`

`python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. location.proto`

python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. location.proto


https://titanssword.github.io/2018-07-26-grpc.html