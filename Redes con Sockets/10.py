import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print("Raw Socket creado correctamente.")
    s.close()
except PermissionError:
    print("Se requieren privilegios de administrador para crear un Raw Socket.")