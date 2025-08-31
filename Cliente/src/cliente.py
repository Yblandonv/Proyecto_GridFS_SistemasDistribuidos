import grpc

from Cliente.stubs import servicios_pb2, servicios_pb2_grpc

def dividir_archivo(ruta_archivo, tamaño_bloque=1024*1024): # Partimos los bloques en 1 MB cada uno
    bloques = []
    with open(ruta_archivo, "rb") as f:
        i = 1
        while True:
        
            datos = f.read(tamaño_bloque)
            
            if not datos:
                break
            
            bloques.append((i, datos))
            i += 1
            
    
    return bloques


def rearmar_archivo(ruta_archivo, bloques):
    
    with open(ruta_archivo, "wb") as img:
        for f in bloques:
            img.write(f[1])


def envio(nombre, bloques):
    channel = grpc.insecure_channel("localhost:8080")

    stub = servicios_pb2_grpc.cliente_nameStub(channel)

    response = stub.guardar_bloques(servicios_pb2.informacion_archivo(nombre_archivo=nombre, numero_bloques=bloques))

    print(response.message)


if __name__ == "__main__":
    bloques = dividir_archivo("Cliente/src/imagen.jpg")

    rearmar_archivo("Cliente/src/resultado.jpg", bloques)

    envio("imagen.png", len(bloques))