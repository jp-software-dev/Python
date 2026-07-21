import socket

HOST = "127.0.0.1"
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Esperando cliente...")

conexion, direccion = servidor.accept()

datos = conexion.recv(1024)
print("Cliente dice:")
print(datos.decode())

conexion.send("Mensaje recibido".encode())
conexion.close()
servidor.close()