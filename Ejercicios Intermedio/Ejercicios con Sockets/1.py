import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Descriptor del socket:", cliente.fileno())

cliente.close()
print("Socket cerrado")