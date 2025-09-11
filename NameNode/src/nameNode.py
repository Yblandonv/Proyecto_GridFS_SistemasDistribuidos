import grpc
import sqlite3

from concurrent import futures
from NameNode.stubs import servicios_pb2, servicios_pb2_grpc



class cliente_nameServicer(servicios_pb2_grpc.cliente_nameServicer):
    def enviar_metadata(self, request, context):
        guardar_bloques(request.nombre_archivo, request.numero_bloques)
        return servicios_pb2.metadata(message=f"Hola, {request.nombre_archivo} {request.numero_bloques}!")


def recibir_peticiones():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_nameServicer_to_server(cliente_nameServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()

def connect_database():
    try:
        sqlite_connection = sqlite3.connect('bloques.db')
        cursor = sqlite_connection.cursor()
        print("DB connected")

        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred -', error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('SQLite Connection closed')
    
def guardar_bloques(nombre_archivo, numero_bloques):
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()
    for i in range(numero_bloques):
        cursor.execute("INSERT INTO bloques (name_block, id_block) VALUES (?, ?)", (nombre_archivo, i))
    conn.commit()
    cursor.close()

def agregar_datanode(ip):
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO datanodes (ip) VALUES (?)", (ip,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_datanodes():
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, ip FROM datanodes")
    datanodes = cursor.fetchall()
    cursor.close()
    conn.close()
    return datanodes

if __name__ == "__main__":
    connect_database()
    recibir_peticiones()