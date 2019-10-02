import socket
import sys
import random
import time

#S_c corresponde al socket que escucha al Cliente
#S_di corresponde al socket que se conecta a los datanodes 1,2,3 en el puerto especifico.
s_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_d1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_d2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_d3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_d1.connect(('datanode1',5001))
s_d2.connect(('datanode2',5002))
s_d3.connect(('datanode3',5003))
s_c.bind(('headnode',5000))
s_c.listen(1)
archivo = open("registro_server.txt","w")
#Se acepta la conexion del cliente
conn_c,addr_c = s_c.accept()
print("Cliente con direccion IP:",addr_c[0],"se ha conectado")
while True:
    print("Esperando mensajes")
    data = conn_c.recv(4096)
    if data.decode('utf-8')=='exit':
        print("No hay mas mensajes")
        #Comunicarle a los demas datanode que no hay mas mensajes para poder cerrar.
        s_d1.send(data)
        s_d2.send(data)
        s_d3.send(data)
        break;
    string=data.decode('utf-8')
    print("Recibido el mensaje:'",string,"',desde la direccion Ip:",addr_c[0])
    datanode_random = random.randint(1,3)
    print("El mensaje se ha guardado en el datanode: ",str(datanode_random))
    #Se manda al datanode1 el mensaje y se recibe la confirmacion luego desde el DataNode1
    if datanode_random == 1:
        s_d1.send(data)
        confirmacion = s_d1.recv(4096)
        print("DataNode1:",confirmacion.decode('utf-8'))
    #Se manda al datanode2 el mensaje y se recibe la confirmacion luego desde el DataNode2
    if datanode_random == 2:
        s_d2.send(data)
        confirmacion = s_d2.recv(4096)
        print("DataNode2:",confirmacion.decode('utf-8'))
    #Se manda al DataNode3 el mensaje y se recibe la confirmacion luego desde el DataNode3
    if datanode_random == 3:
        s_d3.send(data)
        confirmacion = s_d3.recv(4096)
        print("DataNode3",confirmacion.decode('utf-8'))
    #Se escribe en el archivo registro_server.txt donde se guardo el mensaje
    archivo.write("El mensaje:'"+string+"'se ha guardado en el datanode: "+str(datanode_random)+"\n")
    mensaje="El mensaje '"+string+"'fue recibido correctamente y guardado en el datanode "+str(datanode_random)
    #Se envia al cliente el mensaje de confirmacion del mensaje y donde fue guardado.
    conn_c.send(mensaje.encode('utf-8'))
#Se cierran los sockets y el archivo.
conn_c.close()
s_d1.close()
s_d2.close()
s_d3.close()
archivo.close()
print("Cliente",addr_c,"se ha desconectado")
print("Se cierra el servidor")
