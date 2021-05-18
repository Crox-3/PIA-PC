import os
import sys
import traceback
try:
    from PIL.ExifTags import TAGS, GPSTAGS
    from PIL import Image
except ImportError:
    os.system('pip install -r requirements.txt')
    print('\nInstalando los paquetes indicados en "requirements.txt"...')
    print('Ejecuta de nuevo el script.')
    exit()


def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2] 
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}
        input()

 
def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret
    
def printMeta(ruta):
    # Probamos si existe la ruta indicada
    try:
        # Si existe. Nos movemos a ella y creamos el archivo de reporte
        os.chdir(ruta)
        print("*** Iniciando análisis de metadata... *** ")
        archivo = open("Reporte_Metadata.txt","w")
        archivo.write("Metadata de cada imagen incluída en esta carpeta:\n")
        archivo.close()
        # Analizamos todas las rutas y archivos que hay en esta ruta
        for root, dirs, files in os.walk(".", topdown=False):
            # Damos espacio de reporte a cada archivo encontrado
            for name in files:
                name = os.path.join(root, name)
                archivo = open("Reporte_Metadata.txt","a+")
                archivo.write("\nImagen: %s\n" %name)
                archivo.close()
                # Sacamos su metadata si es imagen
                try:
                    exifData = {}
                    exif = get_exif_metadata(name)
                    # Guardamos dato por dato en el reporte
                    for metadata in exif:
                        archivo = open("Reporte_Metadata.txt","a+")
                        archivo.write("Metadata: %s - Value: %s \n" %(metadata, exif[metadata]))
                        archivo.close()
                # No era imagen. Lo indicamos
                except:
                    archivo = open("Reporte_Metadata.txt","a+")
                    archivo.write("Este archivo no es una imagen.")
                    archivo.close()
                    #import sys, traceback
                    #traceback.print_exc(file=sys.stdout)
        print("\n*** Reporte creado en la carpeta analizada. ***")
    # La ruta no era valida. Lo indicamos
    except:
        traceback.print_exc(file=sys.stdout)
        print("\nRUTA INVALIDA. NO SE PUDO ANALIZAR METADATA.")
