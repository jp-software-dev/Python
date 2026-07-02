import socket

print("Creando socket...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket creado")

s.close()
print("Socket cerrado correctamente")