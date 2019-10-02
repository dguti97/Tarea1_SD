import socket

#Se crea el socket del datanode escuchando en el puerto 5002 para que el Headnode se conecte
datanode2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datanode2.bind(('datanode2',5002))
datanode2.listen(1)
#Se acepta la conexion del headnod
archivo= open("./data.txt","w")
while True:
    conn_h,addr_h = datanode2.accept()
    #Recibe el mensaje que el Headnode recibio del Cliente
    received=conn_h.recv(4096)
    string=received.decode('utf-8')
    if(string=='exit'):
        print("Cerrando conexion")
        break;
    #Escribe en el archivo el mensaje del cliente
    archivo.write(string+"\n")
    print(string)
    #Avisa al Headnode que el registro fue correcto
    mensaje="El registro fue correcto"
    conn_h.send(mensaje.encode('utf-8'))
datanode2.close()
archivo.close()
