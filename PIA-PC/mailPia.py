import argparse, email, smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sys
import traceback


def Correo(remitente, password, destinatario, adjunto):
    print("___ Ejecutando el programa mailPia... ___")
    
    asunto = "Imagen Enviada por python"
    cuerpo = "Esta es una imagen enviada por python"

    # Creamos el objeto multipart del correo que enviaremos
    msj = MIMEMultipart()
    msj["From"] = remitente
    msj["To"] = destinatario
    msj["Subject"] = asunto

    # Agregamos el cuerpo al correo
    msj.attach(MIMEText(cuerpo, "plain"))

    archivo = adjunto  

    # Intentamos abrir la imagen en modo de lectrua binaria
    try:
        with open(archivo, "rb") as adjunto:
            msj_adj = MIMEImage(adjunto.read())
            msj_adj.add_header("Content-Disposition", f"adjunto; archivo = {archivo}",)
    except:
        traceback.print_exc(file=sys.stdout)
        print("\nERROR. La imagen no existe o no se pudo abrir.")
    
    # Concatenamos el adjunto codificado con el mensaje 
    msj.attach(msj_adj)
    msj_final = msj.as_string()

    # Intentamos logearnos en el servidor usando una conexion ssl segura
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msj_final)
            print("\n___Correo enviado con exito.___")
    except:
        traceback.print_exc(file=sys.stdout)
        print("\nOcurrio un error inesperado. No se pudo enviar el correo.")
