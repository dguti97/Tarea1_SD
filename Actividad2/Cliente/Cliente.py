import socket
import time

#Se crea el socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Se abre el archivo registro_cliente. Se reemplaza si antes ya existia.
archivo= open("./registro_cliente.txt","w")
#Se conecta el socket al  Headnode en el puerto 5000
client.connect(('headnode', 5000))
#Lista de losmensajes por defecto que se enviaran al Headnode
lista = ["Hola Servidor!","¿Como estas?","Me aburri","exit"]
pos=0
#Se realiza un while recorriendo la lista hasta llegar a la palabra exit.
while True:
    message=lista[pos]
    #Si el mensaje es exit, se notifica al servidor que se acaba la conexion.
    if message=='exit':
        client.send(message.encode('utf-8'))
        break;
    #Se envia el mensaje al servidor
    client.send(message.encode('utf-8'))
    print("El siguiente mensaje ha sido enviado al servidor:",message)
    #Se recibe la notificacion del servidor y tambien donde fue guardado el mensaje.
    received= client.recv(4096)
    string2=received.decode('utf-8')
    archivo.write(string2+"\n")
    print(string2)
    #Se continua con el siguiente mensaje.
    pos=pos+1
    #Se demorara 5 segundos en mandar el siguiente mensaje, esto para que se pueda ver el multicast en accion.
    time.sleep(5)
#Se Cierra la Conexion.
print("Cliente se desconecta")
client.close()
