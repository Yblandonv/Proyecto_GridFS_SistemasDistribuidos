import grpc

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from concurrent import futures

from DataNode.stubs import servicios_pb2, servicios_pb2_grpc

class cliente_dataServicer(servicios_pb2_grpc.cliente_dataServicer):

    def enviar_bloques(self, request, context):
        return servicios_pb2.confirmacion(message=f"Se recibio el bloque: {request.id}!")
    

def recibir_bloque():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_dataServicer_to_server(cliente_dataServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()


def main():
    recibir_bloque()

if __name__ == "__main__":
    main()