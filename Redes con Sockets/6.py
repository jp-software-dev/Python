import socket

host = "google.com"
ip = socket.gethostbyname(host)

print(ip)