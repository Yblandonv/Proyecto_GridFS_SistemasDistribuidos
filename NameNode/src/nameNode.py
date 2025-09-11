import grpc

from concurrent import futures
from NameNode.stubs import servicios_pb2, servicios_pb2_grpc



class cliente_nameServicer(servicios_pb2_grpc.cliente_nameServicer):
    def enviar_metadata(self, request, context):
        return servicios_pb2.metadata(message=f"Hola, {request.nombre_archivo} {request.numero_bloques}!")


def recibir_peticiones():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_nameServicer_to_server(cliente_nameServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()




if __name__ == "__main__":
    recibir_peticiones()