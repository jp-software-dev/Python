import requests
import time
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_datos_cripto():
    url = "https://api.coincap.io/v2/assets?limit=10"
    
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status() 
        datos = respuesta.json()
        return datos['data']
    except requests.exceptions.RequestException as e:
        print(f"[-] Error de conexion: {e}")
        return None

def mostrar_tabla(criptomonedas):
    print("\n" + "="*60)
    print(f"{'RANK':<5} | {'MONEDA':<15} | {'SIMBOLO':<8} | {'PRECIO (USD)':<12} | {'CAMBIO 24H'}")
    print("="*60)
    
    for moneda in criptomonedas:
        rank = moneda['rank']
        nombre = moneda['name'][:15]
        simbolo = moneda['symbol']
        precio = float(moneda['priceUsd'])
        cambio = float(moneda['changePercent24Hr'])
        
        simbolo_cambio = "▲" if cambio > 0 else "▼"
        color_inicio = "\033[92m" if cambio > 0 else "\033[91m"
        color_fin = "\033[0m"
        
        print(f"{rank:<5} | {nombre:<15} | {simbolo:<8} | ${precio:<11.2f} | {color_inicio}{simbolo_cambio} {abs(cambio):.2f}%{color_fin}")
    print("="*60)

def main():
    while True:
        limpiar_pantalla()
        print("TRACKER DE CRIPTOMONEDAS EN TIEMPO REAL")
        print("Obteniendo datos de la red...\n")
        
        criptos = obtener_datos_cripto()
        
        if criptos:
            mostrar_tabla(criptos)
            print("\nActualizando automaticamente en 10 segundos... (Presiona Ctrl+C para salir)")
        
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[+] Saliendo del visualizador. ¡Hasta luego!")