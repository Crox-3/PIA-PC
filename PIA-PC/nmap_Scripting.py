import os
import csv
import argparse
try:
    import nmap
except ImportError:
    os.system('pip install -r requirements.txt')
    print('\nInstalando los paquetes indicados en "requirements.txt"...')
    print('Ejecuta de nuevo el script.')
    exit()

def nmapRun(gatewayip):
    #Escaneo de ip de router

    scanner = nmap.PortScanner()

    targets_List = []
    scanner.scan(hosts=gatewayip +'/24', arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, scanner[x]['status']['state']) for x in scanner.all_hosts()]
    for host, status in hosts_list:
        targets_List.append(host)
    print(targets_List)
    print('\n')

    #Escaneo de ipv4 de dispositivos conectados a el router

    being = 70
    end = 80
    result_Puertos = []
    for host in targets_List:
        print(host + '\n')
        puertos_por_ip = []
        puertos_por_ip.append(host)
        for i in range(being, end+1):
            while True:
                try:    
                    res = scanner.scan(host, str(i))
                    res = res['scan'] [host] ['tcp'] [i] ['state']
                    print (f'port {i} is {res}.')
                    puertos_por_ip.append(f'port {i} is {res}.')
                    break
                except KeyError:
                    print("Ocurrio un error")
    
        result_Puertos.append(puertos_por_ip)
        print('\n')

    print("Escaneo completado\n")
    print("Creando archivo CSV...\n")

    #Creando archivo csv con datos arrojados
    with open('ReporteNmap.csv', 'wt', newline='') as file :
        archivoCsv = csv.writer(file, delimiter='\n')
        archivoCsv.writerow(result_Puertos)

    file.close()
    print("Archivo guardado con exito")