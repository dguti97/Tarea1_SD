import socket
datanode2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datanode2.bind(('datanode2',5002))
datanode2.listen(1)
conn_h,addr_h = datanode2.accept()
archivo= open("./data.txt","w")
while True:
    received=conn_h.recv(4096)
    string=received.decode('utf-8')
    if(string=='exit'):
        print("Cerrando conexion")
        break;
    archivo.write(string+"\n")
    print(string)
    mensaje="El registro fue correcto"
    conn_h.send(mensaje.encode('utf-8'))
datanode2.close()
archivo.close()
