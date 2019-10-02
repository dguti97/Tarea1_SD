import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
arc= open("./respuestas.txt","w")
client.connect(('server', 5000))
lista = ["Hola Servidor","Hola denuevo!","exit"]
cont=0
while True:
    message=lista[cont]
    #message=input("Ingrese su mensaje (exit para salir):")
    if message=='exit':
        client.send(message.encode('utf-8'))
        print("Cliente se desconecta")
        break;
    client.send(message.encode('utf-8'))
    print("El siguiente mensaje ha sido enviado al servidor:",message)
    received= client.recv(4096)
    string2=received.decode('utf-8')
    arc.write(string2+"\n")
    print(string2)
    cont=cont+1
client.close()
arc.close()
