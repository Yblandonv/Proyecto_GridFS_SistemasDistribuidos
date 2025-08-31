import grpc

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from concurrent import futures

from DataNode.stubs import servicios_pb2, servicios_pb2_grpc

class cliente_nameServicer(servicios_pb2_grpc.cliente_nameServicer):
    def guardar_bloques(self, request, context):
        return servicios_pb2.asignacion(message=f"Adios, {request.nombre_archivo} {request.numero_bloques}!")
    
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
servicios_pb2_grpc.add_cliente_nameServicer_to_server(cliente_nameServicer(), server)
server.add_insecure_port("[::]:8080")
server.start()
server.wait_for_termination()