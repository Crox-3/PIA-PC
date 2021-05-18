import hashlib
import os
import argparse
import sys
import traceback


#Funcion HashTool
def HashTool(ruta):
    print("\n°°° Generando el hash del archivo indicado... °°°")
    try:
        file_obj = open(ruta, "rb")
        file = file_obj.read()
        
        Hash = hashlib.sha512(file)
        print(Hash)
        Hashed = Hash.hexdigest()
        print(Hashed)
        print("°°° Hash SHA-512 Completado! °°°")
    except:
        traceback.print_exc(file=sys.stdout)
        print("\nRUTA INVALIDA. No se pudo generar el hash.")
