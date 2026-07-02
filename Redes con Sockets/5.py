import socket

ip = "192.168.1.10"

binario = socket.inet_aton(ip)
print(binario)

texto = socket.inet_ntoa(binario)
print(texto)