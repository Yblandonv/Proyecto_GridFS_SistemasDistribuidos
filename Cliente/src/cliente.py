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
            img.write(f[1])


def envio_archivo(nombre, num_bloques, ip, port): # Cliente -- NameNode

    channel = grpc.insecure_channel(f"{ip}:8080")

    stub = servicios_pb2_grpc.cliente_nameStub(channel)

    response = stub.enviar_metadata(servicios_pb2.informacion_archivo(nombre_archivo=nombre, numero_bloques=num_bloques))

    return response.message


def envio_bloques(bloque, ip): # Cliente -- DataNode
    channel = grpc.insecure_channel(f"{ip}:8080")

    stub = servicios_pb2_grpc.cliente_dataStub(channel)

    response = stub.enviar_bloques(servicios_pb2.informacion_bloque(bloque=bloque[2], id=bloque[1], nombre=bloque[0]))

    print(response.message)
    

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

def main():
    if len(sys.argv) > 1:
        
        ruta_image = sys.argv[1]

        
        bloques = dividir_archivo(ruta_image)

        asignacion = envio_archivo(ruta_image, len(bloques), get_ip(), get_port())

        i = 0
        for bloque in bloques:
            envio_bloques(bloque, asignacion[i])
            i +=1

        #rearmar_archivo("resultado.jpg", bloques)
    else:
        print("Por favor, proporciona la ruta valida de la imagen.")
        


if __name__ == "__main__":
    main()