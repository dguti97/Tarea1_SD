import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
archivo= open("./registro_cliente.txt","w")
client.connect(('headnode', 5000))
message="Hola Servidor"
lista = ["mensaje1","mensaje2","exit"]
cont=0
while True:
    message=lista[cont]
    #message=input("Ingrese su mensaje (exit para salir):")
    if message=='exit':
        client.send(message.encode('utf-8'))
        break;
    client.send(message.encode('utf-8'))
    print("El siguiente mensaje ha sido enviado al servidor:",message)
    received= client.recv(4096)
    string2=received.decode('utf-8')
    archivo.write(string2+"\n")
    print(string2)
    cont=cont+1
print("Cliente se desconecta")
client.close()
