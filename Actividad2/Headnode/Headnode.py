import socket
import sys
import random
import time
import os
import threading
from collections import deque
from heapq import heappush, heappop
from queue import LifoQueue
import subprocess

#Hearbeat: Realiza un ping a cada datanode luego de 5 segundos para saber si estan vivos.
#La variable is_up indica si estan vivos. (0 = vivo, 1 = caido)
#Ademas, se agrega al archivo hearbeat_server.txt los nodos activos cada 5 segundos.
def hearbeat():
    if not q.empty():
        if len(q.get()) == 0:
            return
    t = threading.Timer(5.0, hearbeat)
    t.start()
    hearbeat_server = open("hearbeat_server.txt", "a")
    Node_actives = []
    Node_hostname = ['datanode1', 'datanode2', 'datanode3']
    for i in range(1,4):
        hostname = Node_hostname[i-1]
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', '-c', '3', hostname],
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
                is_up = 0
            except subprocess.CalledProcessError:
                is_up = 1
        #response = os.system("ping -c 1 " + hostname)
        if is_up == 0:
            hearbeat_server.write(str(i)+" ")
            Node_actives.append(i)
    hearbeat_server.write("\n")
    q.put(Node_actives)

def exec_hearbeat():
    hearbeat()

#S_c corresponde al socket que escucha al Cliente
#S_di corresponde al socket que se conecta a los datanodes 1,2,3 en el puerto especifico.
s_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_c.bind(('headnode',5000))
s_c.listen(1)
archivo = open("registro_server.txt","w")
#Se acepta la conexion del cliente
conn_c,addr_c = s_c.accept()
#Cola q, la cual tendra los datanodes activos. Es Lifo (Last in, First Out)
q = LifoQueue()
#Thread que ejecuta la función exec_hearbeat
exec_hearbeat = threading.Thread(target = exec_hearbeat)
exec_hearbeat.start()


print("Cliente con direccion IP:",addr_c[0],"se ha conectado")
while True:
    print("Esperando mensajes")
    data = conn_c.recv(4096) # Mensaje recibido del cliente
    string=data.decode('utf-8') # Se pasa a string
    if data.decode('utf-8')=='exit': #Comunicarle a los demas datanode que no hay mas mensajes para poder cerrar si el cliente dice exit.
        print("No hay mas mensajes")
        lista = q.get() # Saca los nodos activos de 'q' y crea una conexion con los datanodes correspondientes para mandar el mensaje de salida.
        if 1 in lista:
            s_d1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_d1.connect(('datanode1',5001))
            s_d1.send(data)
            s_d1.close()
        if 2 in lista:
            s_d2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_d2.connect(('datanode2',5002))
            s_d2.send(data)
            s_d2.close()
        if 3 in lista:
            s_d3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_d3.connect(('datanode3',5003))
            s_d3.send(data)
            s_d3.close()
        break;

    print("Recibido el mensaje:'",string,"',desde la direccion Ip:",addr_c[0])
    datanode_random = random.choice(q.get()) # Obtiene un datanode random de la lista de datanode activos.
    print("El mensaje se ha guardado en el datanode: ",str(datanode_random))
    #Se manda al datanode1 el mensaje y se recibe la confirmacion luego desde el DataNode1
    if datanode_random == 1:
        s_d1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_d1.connect(('datanode1',5001))
        s_d1.send(data)
        confirmacion = s_d1.recv(4096)
        print("DataNode1:",confirmacion.decode('utf-8'))
        s_d1.close()
    #Se manda al datanode2 el mensaje y se recibe la confirmacion luego desde el DataNode2
    if datanode_random == 2:
        s_d2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_d2.connect(('datanode2',5002))
        s_d2.send(data)
        confirmacion = s_d2.recv(4096)
        print("DataNode2:",confirmacion.decode('utf-8'))
        s_d2.close()
    #Se manda al DataNode3 el mensaje y se recibe la confirmacion luego desde el DataNode3
    if datanode_random == 3:
        s_d3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_d3.connect(('datanode3',5003))
        s_d3.send(data)
        confirmacion = s_d3.recv(4096)
        print("DataNode3",confirmacion.decode('utf-8'))
        s_d3.close()
    #Se escribe en el archivo registro_server.txt donde se guardo el mensaje
    archivo.write("El mensaje:'"+string+"'se ha guardado en el datanode: "+str(datanode_random)+"\n")
    mensaje="El mensaje '"+string+"'fue recibido correctamente y guardado en el datanode "+str(datanode_random)
    #Se envia al cliente el mensaje de confirmacion del mensaje y donde fue guardado.
    conn_c.send(mensaje.encode('utf-8'))

#Se cierran la conexion con el cliente y el archivo.
conn_c.close()
archivo.close()
print("Cliente",addr_c,"se ha desconectado")
print("Se cierra el servidor")
