Maria Apolo 201573509-3
Diego Gutierrez 201573558-1

Instrucciones:
Ejecutar:
1.(sudo) docker-compose build
2.(sudo) docker-compose up

Rutas de archivos:
registro_cliente.txt -> ./Cliente
registro_server.txt y hearbeat_server.txt -> ./Headnode
data.txt -> ./datanode1 , ./datanode2 , ./Datanode3

Observaciones:
1.Se realizo con pings en lugar de multicast.
2.El cliente manda tres mensajes predeterminados (uno cada 5 segundos).Luego de finalizar los mensajes el servidor y los datanodes terminan.
