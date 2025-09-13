import grpc
import sys, os
import configparser

from Cliente.stubs import servicios_pb2, servicios_pb2_grpc

def dividir_archivo(ruta_archivo, tamaño_bloque=1024*1024): # Partimos los bloques en 1 MB cada uno
    bloques = []
    with open(ruta_archivo, "rb") as f:

        i = 1
        while True:
        
            datos = f.read(tamaño_bloque)
            
            if not datos:
                break
            
            bloques.append((ruta_archivo, f'{ruta_archivo}{i}', datos))
            i += 1
            
    
    return bloques # Se devuelve una lista de tuplas con [ID, Bytes]


def rearmar_archivo(ruta_archivo, bloques):
    
    with open(ruta_archivo, "wb") as img:
        for f in bloques:
            img.write(f)


def peticion_archivo(nombre, num_bloques, ip, metodo, password): # Cliente -- NameNode

    channel = grpc.insecure_channel(f"{ip}:8080")

    stub = servicios_pb2_grpc.cliente_nameStub(channel)

    if metodo:
        response = stub.enviar_metadata(servicios_pb2.informacion_archivo(nombre_archivo=nombre, numero_bloques=num_bloques, password=password))

        return response.message

    else:
        response = stub.pedir_metadata(servicios_pb2.peticion(archivo=nombre, password=password))

        bloques = [list(l.dir_bloques) for l in response.dir_bloques] #Vuelvo la respuesta en un formato lista para facilitar la interacción

        return bloques


def peticion_bloques(bloque, ip, nombre_bloque, nombre_archivo, metodo): # Cliente -- DataNode
    channel = grpc.insecure_channel(f"{ip}:5000")

    stub = servicios_pb2_grpc.cliente_dataStub(channel)

    if metodo:

        response = stub.enviar_bloques(servicios_pb2.informacion_bloque(bloque=bloque[2], id=bloque[1], nombre=bloque[0]))

        return response.message
    
    else:

        response = stub.recibir_bloques(servicios_pb2.peticion_bloque(nombre_archivo=nombre_archivo, nombre_bloque=nombre_bloque))

        return response.bloque


def get_ip():
    config = configparser.ConfigParser()
    config.read('address.config')
    ip = config['nameNode']['ip']

    return ip


def get_port():
    config = configparser.ConfigParser()
    config.read('address.config')
    port = config['nameNode']['port']

    return port


def comunicacion():

    ruta_image = sys.argv[2]
    password = input("Ingrese la contraseña para este archivo: ")

    if sys.argv[1] == "post":

        bloques = dividir_archivo(ruta_image)

        asignacion = peticion_archivo(ruta_image, len(bloques), get_ip(), True, password)

        i = 0
        for bloque in bloques:
            peticion_bloques(bloque, asignacion[i], None, None, True)
            i +=1

    elif sys.argv[1] == "get":
        resultado = peticion_archivo(ruta_image, 0, get_ip(), False, password)
        if not resultado:
                print("Contraseña incorrecta o archivo no encontrado")
                return

        file = []

        for bloque in resultado:
            file.append(peticion_bloques(None, bloque[0], bloque[1], ruta_image, False))

        rearmar_archivo(sys.argv[3], file)  if sys.argv[3] != None else rearmar_archivo("resultado.jpg", file)


    else:
        print("Metodo incorrecto")

            
def main():
    if len(sys.argv) > 2:

        comunicacion()

        
    else:
        print("Por favor, proporcione el comando adecuado sudo python3 -m [get/post] [ruta del archivo] opcional:[ruta donde se guardara la copia del get].")
        


if __name__ == "__main__":
    main()