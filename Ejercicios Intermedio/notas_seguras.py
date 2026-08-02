import json
import os
import hashlib
import getpass

# Constante global con el nombre del archivo donde se guardará todo
ARCHIVO_DB = "base_datos_notas.json"

def limpiar_pantalla():
    # Comando condicional para limpiar la terminal en Windows ('cls') o Linux/Mac ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_db():
    # Si el archivo no existe (primera vez que se abre el programa), devuelve un diccionario vacío
    if not os.path.exists(ARCHIVO_DB):
        return {}
    
    # Abre el archivo en modo lectura ('r') y convierte el texto JSON a un diccionario de Python
    with open(ARCHIVO_DB, 'r') as archivo:
        return json.load(archivo)

def guardar_db(datos):
    # Abre el archivo en modo escritura ('w') sobrescribiendo su contenido
    with open(ARCHIVO_DB, 'w') as archivo:
        # Convierte el diccionario a texto y lo guarda con indentación de 4 espacios para que sea legible
        json.dump(datos, archivo, indent=4)

def encriptar_password(password):
    # Convierte el texto a bytes, le aplica el algoritmo criptográfico SHA-256 y devuelve el código hexadecimal
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(db):
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    
    # .strip() elimina espacios en blanco accidentales al inicio y final del texto
    usuario = input("Crea un nombre de usuario: ").strip()
    
    # Verificamos si la llave (nombre de usuario) ya existe en nuestro diccionario de base de datos
    if usuario in db:
        print("[-] El usuario ya existe. Intenta con otro.")
        return
    
    # Pide la contraseña sin que se vean los caracteres en la pantalla por seguridad
    password = getpass.getpass("Crea una contraseña segura: ")
    
    # Crea la estructura de datos del usuario en el diccionario
    db[usuario] = {
        "password": encriptar_password(password),
        "notas": []
    }
    
    # Llama a la función para guardar los cambios en el archivo físico
    guardar_db(db)
    print("[+] Usuario registrado con éxito.")

def iniciar_sesion(db):
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Usuario: ").strip()
    
    # Si el usuario no existe en las llaves de la base de datos, aborta
    if usuario not in db:
        print("[-] Usuario no encontrado.")
        return None
        
    password = getpass.getpass("Contraseña: ")
    
    # Cifra la contraseña que acaba de teclear el usuario para compararla con la guardada
    password_hash = encriptar_password(password)
    
    # Si los hashes coinciden, significa que la contraseña es correcta
    if db[usuario]["password"] == password_hash:
        print("[+] Acceso concedido.")
        return usuario
    else:
        print("[-] Contraseña incorrecta.")
        return None

def menu_notas(usuario, db):
    # Bucle infinito para mantener al usuario dentro de su cuenta hasta que decida salir
    while True:
        limpiar_pantalla()
        print(f"=== BÓVEDA DE NOTAS DE: {usuario.upper()} ===")
        print("1. Ver mis notas")
        print("2. Escribir nueva nota")
        print("3. Cerrar sesión")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            print("\n--- TUS NOTAS ---")
            # Extrae la lista de notas del diccionario correspondiente a este usuario
            notas = db[usuario]["notas"]
            
            if not notas:
                print("No tienes notas guardadas aún.")
            else:
                # Recorre la lista de notas numerándolas, empezando desde el 1
                for i, nota in enumerate(notas, 1):
                    print(f"{i}. {nota}")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '2':
            nueva_nota = input("\nEscribe tu nota: ")
            
            # Agrega la nota a la lista en la memoria RAM
            db[usuario]["notas"].append(nueva_nota)
            
            # Sincroniza la RAM con el archivo físico en el disco duro
            guardar_db(db)
            print("[+] Nota guardada.")
            input("Presiona Enter para continuar...")
            
        elif opcion == '3':
            print("[*] Cerrando sesión...")
            break # Rompe este bucle y devuelve el control a la función main()

def main():
    # Al iniciar el programa, carga la base de datos una sola vez
    db = cargar_db()
    
    while True:
        limpiar_pantalla()
        print("🛡️ SISTEMA DE NOTAS CIFRADAS")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == '1':
            usuario_activo = iniciar_sesion(db)
            # Si iniciar_sesion devolvió un nombre (y no 'None'), entra al menú de notas
            if usuario_activo:
                input("\nPresiona Enter para entrar a tu bóveda...")
                menu_notas(usuario_activo, db)
            else:
                input("\nPresiona Enter para volver al menú...")
                
        elif opcion == '2':
            registrar_usuario(db)
            input("\nPresiona Enter para volver al menú...")
            
        elif opcion == '3':
            print("\n[+] Sistema cerrado de forma segura.")
            break

if __name__ == "__main__":
    main()