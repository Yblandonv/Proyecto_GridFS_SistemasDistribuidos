import grpc

from Cliente.stubs import servicios_pb2, servicios_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")

stub = servicios_pb2_grpc.GreeterStub(channel)

response = stub.SayHello(servicios_pb2.HelloRequest(name="Santiago", surname="Sanchez"))

print(response.message)