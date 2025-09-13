import grpc
import sqlite3

from concurrent import futures
from NameNode.stubs import servicios_pb2, servicios_pb2_grpc

from itertools import cycle

import configparser

class cliente_nameServicer(servicios_pb2_grpc.cliente_nameServicer):
    def enviar_metadata(self, request, context):
        asignaciones = asignar_datanodes(request.nombre_archivo, request.numero_bloques)
        
        return servicios_pb2.metadata(message=asignaciones)
    
    def pedir_metadata(self, request, context):
        bloques = obtener_bloques(request.archivo)

        return servicios_pb2.lista_bloques(dir_bloques=bloques)

def recibir_peticiones():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicios_pb2_grpc.add_cliente_nameServicer_to_server(cliente_nameServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()
    
def guardar_bloques(nombre_archivo, i, ip):
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bloques (name_bloque, name_archivo, ip_asignada) VALUES (?, ?, ?)", (f'{nombre_archivo}{i+1}', nombre_archivo, ip))

    conn.commit()
    cursor.close()

def asignar_datanodes(nombre_archivo, num_bloques):
    #Metodo usado round robin
    
    data_nodes = obtener_datanodes()

    asignaciones = []

    aux = 0
    for ip in cycle(data_nodes):
        guardar_bloques(nombre_archivo, aux, ip[0])
        asignaciones.append(ip[0])
        aux += 1
        if aux == num_bloques:
            break

    return asignaciones

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

    cursor.execute("SELECT ip FROM datanodes")
    datanodes = cursor.fetchall()

    cursor.close()
    conn.close()

    return datanodes

def obtener_bloques(nombre_archivo):
    conn = sqlite3.connect('bloques.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT ip_asignada, name_bloque FROM bloques WHERE name_archivo = ?", (nombre_archivo,))
    datanodes = cursor.fetchall()

    bloques = []

    for bloque in datanodes:
        aux = servicios_pb2.lista()
        aux.dir_bloques.extend(bloque)
        bloques.append(aux)

    print(bloques)

    cursor.close()
    conn.close()

    return bloques

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
    borrar_datanode()
    
    for i in range(3):
        ip = get_ip(i)
        agregar_datanode(ip)

    recibir_peticiones()
    