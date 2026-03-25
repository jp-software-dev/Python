import qrcode
import os

def generar_qr_limpio(datos, ruta_salida):
    
    qr = qrcode.QRCode(
        version=None, 
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(datos)
    qr.make(fit=True)

    # Crear la imagen del QR
    img_qr = qr.make_image(fill_color="black", back_color="white")

    # Guardar el resultado
    img_qr.save(ruta_salida)
    print(f"[+] QR Generado con éxito: {os.path.basename(ruta_salida)}")


if __name__ == "__main__":
    # Detectar la carpeta donde está este script
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Lista de adivinanzas (el texto que se verá al escanear)
    pistas = [
        {
            "texto": "I have many leaves, but I am no tree. I have many stories, but I cannot speak. People come to me when they need quiet and knowledge. Where am I?",
            "salida": "QR_1.png"
        },
        {
            "texto": "This is where logic meets design, and builders of the future align their plans. Whether it is for systems, code, or machines, you come here to organize your academic routines. Where am I?",
            "salida": "QR_2.png"
        },
        {
            "texto": "I am the place where your coins say goodbye, so your education can fly high. You visit me to settle your debt, making sure your semester is perfectly set. Where am I?",
            "salida": "QR_3.png"
        },
        {
            "texto": "I am a room full of crowns, but there are no kings. I have special chairs and bright lights that gleam. Open wide and show your smile, you might be sitting here for a while. Where am I?",
            "salida": "QR_4.png"
        }
    ]

    print(f"--- Iniciando generación de QRs limpios en: {base_path} ---\n")

    for pista in pistas:
        # Definimos dónde se va a guardar
        path_output = os.path.join(base_path, pista["salida"])
        
        # Llamamos a la función enviando solo el texto y la ruta de salida
        generar_qr_limpio(pista["texto"], path_output)

    print("\n--- Tarea completada. Tienes tus 4 QRs listos para imprimir. ---")