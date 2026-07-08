import requests
import time
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_datos():
    # URL principal de la API de CoinGecko para obtener precios de criptomonedas
    url = "https://api.coingecko.com/api/v3/simple/price"

    # Parámetros de la solicitud para obtener los precios en USD y el cambio en 24 horas
    parametros = {
        "ids": "bitcoin,ethereum,ripple,cardano,solana,dogecoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        # Realizamos la petición a internet agregando los parámetros y un tiempo límite de espera
        respuesta = requests.get(url, params=parametros, timeout=10)
        # Verificamos si la respuesta fue exitosa o no, y en caso de error, se lanza una excepción
        respuesta.raise_for_status()
        # Convierte la respuesta en formato JSON y la retorna
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print(f"[-] Error de conexión: {e}")
        return None
# Función para mostrar la información de las criptomonedas en formato de tabla
def mostrar_tabla(datos):
    print("\n" + "="*55)
    print(f"{'CRIPTOMONEDA':<15} | {'PRECIO (USD)':<15} | {'CAMBIO 24H'}")
    print("="*55)

    # Se recorre cada criptomoneda y se imprime su información en formato de tabla
    for moneda, info in datos.items():
        nombre = moneda.capitalize()
        precio = info.get("usd", 0.0)
        cambio = info.get("usd_24h_change", 0.0)

        simbolo = "▲" if cambio > 0 else "▼"
        color = "\033[92m" if cambio > 0 else "\033[91m"
        reset = "\033[0m"
        
        # imprime la información de la criptomoneda en formato de tabla
        print(f"{nombre:<15} | ${precio:<14.2f} | {color}{simbolo} {abs(cambio):.2f}%{reset}")
    print("="*55)

def main():
    # Bucle que actualiza la información cada 15 segundos
    while True:
        limpiar_pantalla()
        print("TRACKER DE CRIPTOMONEDAS")
        print("Obteniendo datos de la red...\n")
        
        # Llamamos a la función de internet
        datos = obtener_datos()

        # Si la petición fue exitosa, mostrar la tabla de precios y cambios
        if datos:
            mostrar_tabla(datos)
            print("\nActualizando en 15 segundos...")
        
        # Pause el programa durante 15 segundos antes de la siguiente actualización
        time.sleep(15)

# Punto de entrada del programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[+] Saliendo del visualizador. ¡Hasta luego!")