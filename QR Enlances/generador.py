import qrcode

# Definir una función que crea y guarda un código QR a partir de un texto/enlace
def generar_qr_simple(datos, ruta_salida):
    
    # Configuración del generador de QR
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10, 
        border=4, 
    )
    
    # Añadir los datos (en este caso, la URL) a la configuración del QR
    qr.add_data(datos)
    # Ajustar automáticamente las dimensiones para que los datos quepan correctamente
    qr.make(fit=True)

    # Crear la imagen del QR especificando los colores (blanco y negro estándar)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen generada en la ruta proporcionada
    img_qr.save(ruta_salida)
    
    # Mostrar un mensaje en la consola para confirmar que terminó el proceso
    print(f"¡Éxito! Código QR de enlace guardado en: {ruta_salida}")

# Bloque principal que se ejecuta al correr el script
if __name__ == "__main__":

    # Definir el enlace que se almacenará dentro del código QR
    texto_qr = "https://perfil-dev-software.vercel.app/"
    # Definir el nombre del archivo de imagen resultante
    archivo_salida = "QR.png"

    # Llamar a la función pasando los datos y el nombre del archivo
    generar_qr_simple(texto_qr, archivo_salida)