import socket

HOST = "127.0.0.1"
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor esperando...")

conexion, direccion = servidor.accept()

mensaje = conexion.recv(1024)

print("Cliente:", mensaje.decode())

conexion.send("Hola cliente".encode()) 

conexion.close()
servidor.close()