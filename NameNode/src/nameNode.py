import grpc

from concurrent import futures

from NameNode.stubs import servicios_pb2, servicios_pb2_grpc

class GreeterServicer(servicios_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return servicios_pb2.HelloReply(message=f"Hola, {request.name} {request.surname}!")
    
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
servicios_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
server.add_insecure_port("[::]:8080")
server.start()
server.wait_for_termination()