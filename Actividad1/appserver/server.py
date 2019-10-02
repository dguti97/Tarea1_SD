import socket
import time

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('server', 5000))
serv.listen(1)
archivo = open("./logs.txt","w")
while True:
    print("Servidor iniciado,esperando clientes")
    conn, addr = serv.accept()
    while True:
        data = conn.recv(4096)
        if data.decode('utf-8') == 'exit':
            print("Cliente",addr,"se ha desconectado")
            break
        string=data.decode('utf-8')
        archivo.write(str(addr[0])+" "+string+"\n")
        print("Recibido el mensaje:'",string,"',desde la direccion Ip y Puerto:",addr)
        mensaje="El mensaje "+string+" fue recibido correctamente"
        conn.send(mensaje.encode('utf-8'))
    conn.close()
    print("Se cierra el servidor")
    break;
archivo.close()
