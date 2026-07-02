import socket

HOST = "example.com"
PORT = 80

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

peticion = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
cliente.send(peticion.encode())

print(cliente.recv(2048).decode())

cliente.close()