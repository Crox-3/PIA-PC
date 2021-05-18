# PIA-PC
# Múltiples Herramientas de Ciberseguridad  
import argparse
import subprocess
import os
import logging
import socket
import sys
import traceback
try:
    from googlesearch import search
except ImportError:
    os.system('pip install -r requirements.txt')
    print('\nInstalando los paquetes indicados en "requirements.txt"...')
    print('Ejecuta de nuevo el script.')
    exit()

# Funciones de modulos locales
from Metadata_Script import printMeta
from nmap_Scripting import nmapRun
from mailPia import Correo
from Hash_Script import HashTool


def main(firewallOpc):
    # Condicion que valida si el usuario quiso usar la herramienta FirewallRed
    if(firewallOpc!="Nada"):
        # Llamado a la funcion interna de Firewall
        FirewallRed(firewallOpc)


def FirewallRed(opc):
    print("\n\n--- Corriendo el programa FirewallRed... ---")
    # Validamos que sea una opcion correcta
    if(opc == "Status" or opc == "Public" or opc == "Private"):
        # Llamado a la aplicacion Powershell externa de FirewallRed 
        psExe = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                                  '-ExecutionPolicy',
                                  'Unrestricted',
                                  './PS_Scripts/FirewallRedInfo.ps1', #Checar esto
                                  opc], cwd=os.getcwd())
        psExe.wait()
        print("\n")
    else:
        print("ERROR. Corra de nuevo este script con una opcion firewall correcta.")


def SocketInfo(hostname):
    print("=== Inicio de la aplicacion SocketInfo... ===\n")
    try:
        info = socket.gethostbyname_ex(hostname)
        print("Info del dominio: " + str(info))
        print("\nResultados de buscar este dominio en Google: ")
        query = info[0]
        for enlace in search(query, tld="com", num=10, stop=10, pause=2):
            print(enlace)
        print("\n=== Fin de la busqueda ===")
    except:
        traceback.print_exc(file=sys.stdout)
        print("\nLINK INVALIDO. No se pudo analizar ningun host.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Herramientas de ciberseguridad')
    
    parser.add_argument('--hash', '-H', 
                        help='Ruta completa del archivo que deseamos "hashear".')
    
    parser.add_argument('--metadata', '-M', type=str, 
                        help='Ver metadatos de las imagenes \
                            de la carpeta indicada.')
    
    parser.add_argument('--nmap', '-N', 
                        help='Escanear puertos IP (no olvides \
                        ingresar el argumento --gatewayip).', 
                        action='store_true')
    
    parser.add_argument('--gatewayip', '-GWI', type=str, 
                        help='Ingresar su puerta de enlace(Gateway Ip).')
    
    parser.add_argument('--firewall', '-F', type=str, 
                        help='La opcion que desea \
                        realizar con el tipo de red (checar documentacion).', 
                        default='Nada')
    
    parser.add_argument('--hostname', '-H2', type=str, 
                        help='Link del host que quiere analizar.')
    
    # Argumentos para el envío de correo.
    parser.add_argument("--remitente", "-r1", 
                        dest = "remitente", 
                        type = str,
                        default = "programa.segu@gmail.com",
                        help = "Correo del remitente")
    
    parser.add_argument("--pswd", "-p",
                        dest = "pswd",
                        type = str,
                        default = "PiaPseguridad",
                        help = "Contraseña del remitente")
    
    parser.add_argument("--destinatario", "-d",
                        dest = "destinatario",
                        type = str, 
                        help = "Correo del destinatario")
    
    parser.add_argument("--ruta", "-r2",
                        dest = "ruta",
                        type = str, 
                        help = "Ruta del adjunto del correo")
    
    args = parser.parse_args()
    
    # Chequeo de argumentos para hash
    if args.hash:
        logging.info("Hash_Script")
        HashTool(args.hash)
    
    # Chequeo de argumentos para metadata
    if args.metadata:
        logging.info("Metadata_Script")
        printMeta(args.metadata)
    
    # Chequeo de argumentos para nmap
    if args.nmap:
        if args.gatewayip:
            logging.info("nmap_Scripting")
            nmapRun(args.gatewayip)
        else:
            logging.warning("Falta el argumento --gatewayip")
            parser.error("--nmap requires --gatewayip.")
    
    # Chequeo de argumentos para SocketInfo
    if args.hostname:
        logging.info("SocketInfo")
        SocketInfo(args.hostname)
    
    # Chequeo de argumentos para el envio de correos
    if args.destinatario:
        if args.ruta:
            logging.info("mailPia")
            Correo(args.remitente, args.pswd, args.destinatario, args.ruta)
        else:
            logging.warning("Falta algun argumento para el envio de correos.")
    
    main(args.firewall)
