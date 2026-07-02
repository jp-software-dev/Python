import socket

HOST = "127.0.0.1"
PORT = 6000

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.sendto("Hola servidor".encode(), (HOST, PORT))

respuesta, direccion = c.recvfrom(1024)
print(respuesta.decode())