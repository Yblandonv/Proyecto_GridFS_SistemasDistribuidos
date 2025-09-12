import grpc
import sqlite3

from concurrent import futures
from NameNode.stubs import servicios_pb2, servicios_pb2_grpc

import configparser

class cliente_nameServicer(servicios_pb2_grpc.cliente_nameServicer):
    def enviar_metadata(self, request, context):
        guardar_bloques(request.nombre_archivo, request.numero_bloques)
        return servicios_pb2.metadata(message=f"Tu imagen fue guardada con exito!!")


def recibir_peticiones():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_nameServicer_to_server(cliente_nameServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()

    
def guardar_bloques(nombre_archivo, numero_bloques):
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()

    for i in range(numero_bloques):
        cursor.execute("INSERT INTO bloques (name_bloque, id_bloque) VALUES (?, ?)", (f'{nombre_archivo}{i+1}', i+1))

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

def borrar_datanode():
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM datanodes")
    conn.commit()

    cursor.close()
    conn.close()

def get_ip(i):
    config = configparser.ConfigParser()
    config.read('address.config')
    ip = config[f'dataNode{i+1}']['ip']

    return ip


if __name__ == "__main__":
    print("Servidor encendido..\n")
    borrar_datanode() #Borrar las ip de los dataNodes por si cambian con el tiempo
    for i in range(2):
        ip = get_ip(i)
        agregar_datanode(ip)

    recibir_peticiones()
    