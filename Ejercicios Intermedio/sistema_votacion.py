"""
* Descripción del Problema:
* Se requiere desplegar un sistema de auditoría y votación electrónica en terminal.
* El desafío operativo es evitar ataques de repetición o fraude interno (doble voto), 
* validando que un identificador (ID/Matrícula) único no sea procesado más de una vez.
*
* Solución Óptima (Usando Estructuras Hash):
* Se implementa un objeto `set` para registrar los identificadores que ya emitieron su voto.
* Cuando un nuevo ID ingresa, el sistema consulta el `set`. Al usar una arquitectura de tabla hash
* interna, la verificación no requiere recorrer toda la base de datos, bloqueando intentos de 
* fraude de forma instantánea.
*
* Complejidad:
* - Temporal: O(1) promedio para validar IDs y registrar votos. O(C) para mostrar resultados (C = candidatos).
* - Espacial: O(V) donde V es la cantidad de votantes almacenados en memoria durante la sesión.
"""

import os

def limpiar_pantalla():
    # Operación de sistema para limpiar la terminal (compatible con entornos Windows y Unix/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_resultados(candidatos, total_votos):
    print("\n--- RESULTADOS ACTUALES ---")
    
    # Prevención de fallos críticos (División por cero) si se solicitan resultados antes del primer voto
    if total_votos == 0:
        print("Aún no hay votos registrados.")
    else:
        # Iteración sobre el diccionario para procesar métricas de porcentaje en tiempo real
        for candidato, votos in candidatos.items():
            porcentaje = (votos / total_votos) * 100
            print(f"{candidato}: {votos} votos ({porcentaje:.2f}%)")
    print("-" * 27)

def main():
    # Diccionario actuando como base de datos en memoria (clave: candidato, valor: contador de votos)
    candidatos = {"Candidato A": 0, "Candidato B": 0, "Candidato C": 0}
    
    # Estructura Set() utilizada como control de acceso. Ideal en seguridad por su tiempo de búsqueda O(1)
    votantes_registrados = set()
    total_votos = 0

    # Bucle de evento principal (Event Loop) que mantiene la terminal en estado de escucha activa
    while True:
        limpiar_pantalla()
        print("SISTEMA DE VOTACIÓN ELECTRÓNICA")
        print("1. Emitir voto")
        print("2. Ver resultados en vivo")
        print("3. Cerrar votación y salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == '1':
            # Saneamiento de datos de entrada (.strip) y normalización (.upper) para evitar evasión de filtros
            identificador = input("\nIngresa tu ID o Matrícula para votar: ").strip().upper()
            
            # Regla de control lógico: Si el identificador ya existe en el Set, se bloquea la transacción
            if identificador in votantes_registrados:
                print("[-] Error de Seguridad: Este ID ya ha emitido un voto. Transacción rechazada.")
                input("Presiona Enter para continuar...")
                continue # Aborta el flujo actual y reinicia el bucle

            print("\nCandidatos disponibles:")
            
            # Extracción de las llaves del diccionario a un formato indexable numéricamente para el menú
            lista_candidatos = list(candidatos.keys())
            for i, candidato in enumerate(lista_candidatos, 1):
                print(f"{i}. {candidato}")

            voto = input("\nIngresa el número de tu candidato: ")
            
            # Validación de tipo de dato (solo dígitos) y control de rangos para evitar desbordamientos
            if voto.isdigit() and 1 <= int(voto) <= len(lista_candidatos):
                
                # Asignación del voto ajustando el índice base 0 de las listas en Python
                candidato_elegido = lista_candidatos[int(voto) - 1]
                
                # Ejecución de la transacción: se actualizan los contadores y se "quema" el ID del votante
                candidatos[candidato_elegido] += 1
                votantes_registrados.add(identificador) # .add() inyecta el dato al Set
                total_votos += 1
                
                print(f"[+] Voto registrado exitosamente para {candidato_elegido}.")
            else:
                print("[-] Entrada de selección inválida. Proceso abortado.")
            
            input("Presiona Enter para continuar...")

        elif opcion == '2':
            # Llamada a la función de auditoría visual
            mostrar_resultados(candidatos, total_votos)
            input("Presiona Enter para continuar...")

        elif opcion == '3':
            limpiar_pantalla()
            print("CIERRE DE URNA. RESULTADOS OFICIALES AUDITADOS:")
            mostrar_resultados(candidatos, total_votos)
            break # Ruptura segura del bucle principal
            
        else:
            print("[-] Comando no reconocido por el sistema.")
            input("Presiona Enter para continuar...")

# Punto de entrada estándar para proteger la ejecución si el script es importado por otros módulos
if __name__ == "__main__":
    main()