import qrcode
import os

def generar_qr_enlace(url, ruta_salida):
    # 1. Configuración básica de la estructura del QR
    qr = qrcode.QRCode(
        version=None, # Permite que el tamaño se ajuste automáticamente según la longitud del enlace
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Nivel básico de corrección de errores
        box_size=10, # Tamaño de cada "cuadrito" del QR
        border=4,    # Grosor del margen blanco alrededor del QR
    )
    
    # 2. Insertamos el enlace (URL) en el objeto QR
    qr.add_data(url)
    qr.make(fit=True)

    # 3. Generamos la imagen con los colores clásicos
    img_qr = qr.make_image(fill_color="black", back_color="white")
    
    # 4. Guardamos la imagen en la ruta especificada
    img_qr.save(ruta_salida)
    
    print(f"[+] QR Generado con exito: {os.path.basename(ruta_salida)}")

if __name__ == "__main__":
    # Detectamos la ruta exacta donde está guardado este archivo de Python
    base_path = os.path.dirname(os.path.abspath(__file__))

    print("\n--- GENERADOR DE QR PARA ENLACES ---")
    print(f"Tus imagenes se guardaran en: {base_path}")
    print("-" * 40)

    contador = 1 # Usaremos esto para nombrar los archivos (QR_Enlace_1.png, QR_Enlace_2.png, etc.)
    
    # Iniciamos un bucle infinito para que puedas meter todos los enlaces que quieras
    while True:
        # Pedimos el enlace al usuario a través de la consola
        enlace = input("\nIngresa el enlace (o escribe 'salir' para terminar): ").strip()
        
        # Condición para romper el bucle y cerrar el programa
        if enlace.lower() == 'salir':
            print("Cerrando el generador... ¡Hasta luego!")
            break
            
        # Validación de seguridad por si el usuario presiona Enter sin escribir nada
        if not enlace:
            print("[-] Error: El enlace no puede estar vacio. Intenta de nuevo.")
            continue

        # Generamos el nombre del archivo dinámicamente y unimos la ruta
        nombre_archivo = f"QR_Enlace_{contador}.png"
        path_output = os.path.join(base_path, nombre_archivo)
        
        # Llamamos a nuestra función principal pasándole el enlace y dónde guardarlo
        generar_qr_enlace(enlace, path_output)
        
        # Aumentamos el contador para el siguiente QR
        contador += 1