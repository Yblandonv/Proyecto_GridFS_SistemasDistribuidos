import grpc
import os
from dotenv import load_dotenv
from nameNode import serve

if __name__ == "__main__":
    load_dotenv()
    serve()
