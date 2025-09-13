import grpc
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from concurrent import futures
from DataNode.stubs import servicios_pb2, servicios_pb2_grpc

# Directorio base para guardar los archivos en el DataNode
DATA_DIR = "data_datanode"

def guardar_bloque(nombre_archivo, num_bloque, datos_bloque):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    archivo_dir = os.path.join(DATA_DIR, nombre_archivo)
    if not os.path.exists(archivo_dir):
        os.makedirs(archivo_dir)

    bloque_path = os.path.join(archivo_dir, f"{num_bloque}")
    with open(bloque_path, "wb") as f:
        f.write(datos_bloque)

    print(f"[DataNode] Guardado {bloque_path}")

def acceder_bloque(nombre_bloque, nombre_archivo):

    with open(f"./data_datanode/{nombre_archivo}/{nombre_bloque}", "rb") as f:

        datos = f.read()

        return datos


class cliente_dataServicer(servicios_pb2_grpc.cliente_dataServicer):
    def enviar_bloques(self, request, context):
        # Aquí guardamos el bloque recibido
        guardar_bloque(request.nombre, request.id, request.bloque)
        return servicios_pb2.confirmacion(message=f"Se recibió y guardó el bloque: {request.id}!")
    
    def recibir_bloques(self, request, context):
        # Aquí recibimos la petición de get
        
        return servicios_pb2.respuesta_bloque(bloque=acceder_bloque(request.nombre_bloque, request.nombre_archivo))

def recibir_bloque():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_dataServicer_to_server(cliente_dataServicer(), server)
    server.add_insecure_port("[::]:5000")
    server.start()
    server.wait_for_termination()

def main():
    recibir_bloque()

if __name__ == "__main__":
    print("Servidor encendido..\n")
    main()
