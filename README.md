# GridDFS - Sistema de Archivos Distribuido por Bloques

Sistema de archivos distribuido minimalista inspirado en HDFS y GFS, implementado en Python con comunicación gRPC.

## Características

- **Arquitectura Maestro-Trabajador**: Un NameNode central coordina múltiples DataNodes
- **Particionamiento por Bloques**: Archivos divididos en bloques de 1MB
- **Distribución Round-Robin**: Balanceamiento automático de carga
- **Comunicación gRPC**: Protocolo eficiente y confiable
- **Verificación de Integridad**: Checksums automáticos para cada bloque
- **CLI Simple**: Comandos `put` y `get` para subir y descargar archivos

##  Arquitectura

<img width="918" height="773" alt="image" src="https://github.com/user-attachments/assets/ccd83953-813b-468d-962c-a9e8dd2c8981" />


## Inicio Rápido

### Prerequisitos

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install grpcio grpcio-tools

# Verificar instalación
python3 -c "import grpc; print(' gRPC instalado')"
```

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Yblandonv/Proyecto_GridFS_SistemasDistribuidos.git
cd Proyecto_GridFS_SistemasDistribuidos
```

2. **Generar stubs de gRPC**
```bash
cd Cliente
python3 -m grpc_tools.protoc --proto_path=protobufs \
    --python_out=stubs --grpc_python_out=stubs \
    protobufs/servicios.proto

cd ../NameNode
python3 -m grpc_tools.protoc --proto_path=protobufs \
    --python_out=stubs --grpc_python_out=stubs \
    protobufs/servicios.proto

cd ../DataNode
python3 -m grpc_tools.protoc --proto_path=protobufs \
    --python_out=stubs --grpc_python_out=stubs \
    protobufs/servicios.proto
```
**IMPORTANTE**

Agregar 

```bash
from .
```
a cada uno de los imports de grpc 

Ejemplo:
from . import servicios_pb2 as servicios__pb2

3. **Configurar red**
```bash
# Editar con las IPs reales
nano address.config
```

### Ejecución

1. **Iniciar NameNode**
```bash
cd NameNode
python3 -m src.nameNode
```

2. **Iniciar DataNodes** (en máquinas separadas)
```bash
cd DataNode
python3 -m src.dataNode
```

3. **Usar el cliente**
```bash
cd Cliente
# Subir archivo
python3 -m src.cliente post archivo.txt

# Descargar archivo
python3 -m src.cliente get archivo.txt
```

## Comandos Disponibles

### Cliente CLI

```bash
# Subir archivo al sistema distribuido
python3 -m src.cliente post <ruta_archivo>

# Descargar archivo del sistema distribuido
python3 -m src.cliente get <nombre_archivo> [archivo_destino]
```

### Ejemplos de Uso

```bash
# Subir una imagen
python3 -m src.cliente post /home/user/vacation.jpg

# Descargar con nombre específico  
python3 -m src.cliente get vacation.jpg downloaded_vacation.jpg

# Subir documento grande
python3 -m src.cliente post large_dataset.csv
```

## Estructura del Proyecto

```
GridDFS/
├── Cliente/                    # Cliente CLI
│   ├── src/cliente.py         # Lógica principal del cliente
│   ├── stubs/                 # Stubs generados de gRPC
│   └── protobufs/servicios.proto
├── NameNode/                  # Servidor de metadatos
│   ├── src/nameNode.py        # Lógica del NameNode
│   ├── stubs/                 # Stubs generados de gRPC
│   └── protobufs/servicios.proto
├── DataNode/                  # Servidor de almacenamiento
│   ├── src/dataNode.py        # Lógica del DataNode
│   ├── stubs/                 # Stubs generados de gRPC
│   └── protobufs/servicios.proto
├── address.config             # Configuración de red
├── bloques.db                 # base de datos sqlite
└── README.md
```

## Configuración



### address.config

```ini
[nameNode]
ip=34.204.42.155
port=8080

[dataNode1]
ip=123.456.789.321


[dataNode2]  
ip=987.654.321.123


[dataNode3]
ip=456.234.251.123

```

### Parámetros Configurables

- **Tamaño de bloque**: Modificar `tamaño_bloque` en `cliente.py` (default: 1MB)
- **Puerto del servidor**: Cambiar puerto en cada componente (default: 8080)
- **DataNodes**: Agregar/quitar secciones `[dataNodeN]` en configuración

## Pruebas

### Prueba Básica

```bash
# Crear archivo de prueba
echo "Hola GridDFS!" > test.txt

# Subir archivo
python3 -m src.cliente post test.txt

# Descargar archivo
python3 -m src.cliente get test.txt downloaded_test.txt

# Verificar integridad
diff test.txt downloaded_test.txt
echo "✅ Prueba exitosa si no hay diferencias"
```

### Prueba con Archivo Grande

```bash
# Generar archivo de prueba de 10MB
dd if=/dev/zero of=large_file.dat bs=1M count=10

# Subir archivo (se dividirá en ~10 bloques)
python3 -m src.cliente post large_file.dat

# Descargar archivo
python3 -m src.cliente get large_file.dat downloaded_large.dat

# Verificar integridad
md5sum large_file.dat downloaded_large.dat
```

##  Monitoreo del Sistema

### Verificar Estado de los Nodos

```bash
# Ver procesos activos
ps aux | grep -E "(nameNode|dataNode)"

# Ver logs en tiempo real
tail -f NameNode/namenode.log
tail -f DataNode/datanode.log
```

### Consultar Base de Datos de Metadatos

```bash
# Acceder a la base de datos del NameNode
sqlite3 bloques.db

# Consultas útiles
.tables
SELECT * FROM datanodes;
SELECT * FROM archivos;
SELECT * FROM bloques WHERE name_archivo = 'test.txt';
```

##  Tecnologías Utilizadas

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| **Lenguaje** | Python | 3.8+ | Implementación principal |
| **Comunicación** | gRPC | 1.74.0 | Protocolo inter-servicios |
| **Serialización** | Protocol Buffers | 3.x | Definición de mensajes |
| **Base de Datos** | SQLite | 3.x | Metadatos del NameNode |
| **Networking** | TCP | - | Transporte subyacente |

## Algoritmos Implementados

### Particionamiento de Archivos
- **Algoritmo**: División secuencial en bloques de tamaño fijo
- **Tamaño de bloque**: 1 MB (configurable)
- **Identificación**: `<nombre_archivo><numero_bloque>`

### Distribución de Bloques
- **Estrategia**: Round-Robin
- **Ventajas**: Distribución equitativa, simplicidad
- **Balanceamiento**: Automático entre DataNodes disponibles

## Limitaciones Conocidas

### Tolerancia a Fallos
-  **Sin replicación**: Pérdida de DataNode = pérdida de datos
-  **Punto único de falla**: NameNode crítico para el sistema
-  **Sin heartbeat**: No detección automática de nodos caídos

### Escalabilidad
-  **Configuración estática**: DataNodes predefinidos en configuración
-  **Metadatos centralizados**: NameNode puede ser cuello de botella
-  **Sin balanceamiento dinámico**: No considera carga actual de nodos

### Seguridad
-  **Sin autenticación**: Acceso libre al sistema
-  **Sin cifrado**: Datos transmitidos sin protección
-  **Sin autorización**: No control de acceso por usuario

##  Roadmap y Mejoras Futuras

### Versión 1.1
- [ ] Autenticación básica (usuario/contraseña)
- [ ] Comandos adicionales: `ls`, `rm`, `mkdir`, `rmdir`
- [ ] Mejores mensajes de error y logging
- [ ] Dockerización completa del sistema

## Contribuciones

Este proyecto fue desarrollado como parte del curso ST0263. Las contribuciones están limitadas a los miembros del equipo:

- **Santiago Sanchez**: Arquitectura general y CLiente CLI
- **Yasir Blandón**: DataNode y gestión de bloques  
- **Juan Pablo Rúa**: Name node y Documentacion

## Reporte de Issues

Si encuentras problemas durante la ejecución:

1. **Verifica los logs** de cada componente
2. **Revisa la configuración** de red en `address.config`
3. **Confirma que los puertos** estén disponibles
4. **Valida las dependencias** con `pip3 list`

### Issues Comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| "Connection refused" | NameNode no iniciado | Verificar que NameNode esté corriendo |
| "Bloque no encontrado" | DataNode desconectado | Reiniciar DataNode correspondiente |
| "Import Error: grpc" | Dependencias faltantes | `pip3 install grpcio grpcio-tools` |

## Licencia

Este proyecto es desarrollado con fines académicos para el curso ST0263 de la Universidad EAFIT.


**GridDFS v1.0** - Sistema de Archivos Distribuido por Bloques  
Desarrollado por Santiago, Yasir Blandón y Juan Pablo Rúa - Universidad EAFIT 2025
