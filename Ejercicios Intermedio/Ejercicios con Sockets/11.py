from xmlrpc.server import SimpleXMLRPCServer

def sumar(a, b):
    return a + b

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(sumar, "sumar")

print("Servidor RPC esperando llamadas...")
server.serve_forever()