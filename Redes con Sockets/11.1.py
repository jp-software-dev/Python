import xmlrpc.client

cliente = xmlrpc.client.ServerProxy("http://localhost:8000/")
resultado = cliente.sumar(10, 5)

print("Resultado:", resultado)