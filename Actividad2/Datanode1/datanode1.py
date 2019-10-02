import socket

#Se crea el socket del datanode escuchando en el puerto 5001 para que el Headnode se conecte
datanode1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datanode1.bind(('datanode1',5001))
datanode1.listen(1)
#Se acepta la conexion del headnode
conn_h,addr_h = datanode1.accept()
archivo= open("./data.txt","w")
while True:
    #Recibe el mensaje que el Headnode recibio del Cliente
    received=conn_h.recv(4096)
    string=received.decode('utf-8')
    if(string=='exit'):
        print("Cerrando conexion")
        break;
    #Escribe en el archivo el mensaje del cliente
    archivo.write(string+"\n")
    print(string)
    mensaje="El registro fue correcto"
    conn_h.send(mensaje.encode('utf-8'))
datanode1.close()
archivo.close()
