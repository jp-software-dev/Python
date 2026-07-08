# Librería principal para interfaces gráficas y videojuegos
import pygame 
# Manejo de tiempos del sistema
import time   
# Permite generar números aleatorios (usado para ubicar la comida al azar)
import random 

# Inicializa todos los motores internos de la librería Pygame
pygame.init()

# Definimos la paleta de colores usando el formato RGB (Rojo, Verde, Azul)
blanco = (255, 255, 255)
negro = (0, 0, 0)

# Color utilizado para dibujar la cuadrícula de fondo
gris_oscuro = (30, 30, 30) 
rojo = (213, 50, 80)
verde = (0, 255, 0)

# Color utilizado para resaltar el texto de la puntuación
amarillo = (255, 215, 0) 

# Configuración de las dimensiones de la ventana del juego en píxeles
ancho = 600
alto = 400

# Creamos la ventana principal y le asignamos un título que aparecerá en la barra superior
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Juego de la Serpiente')

# Reloj interno para controlar los Fotogramas Por Segundo (FPS) y estabilizar la velocidad
reloj = pygame.time.Clock()

# Tamaño en píxeles tanto de la comida como de cada segmento de la serpiente
tamano_bloque = 10 
# Velocidad a la que corre el juego (15 vueltas por segundo)
velocidad = 15     

# Definimos las fuentes (tipografías) para los diferentes textos en pantalla
fuente_mensajes = pygame.font.SysFont("bahnschrift", 25)
fuente_puntos = pygame.font.SysFont("bahnschrift", 18)


def dibujar_cuadricula():
    # Dibuja líneas verticales separadas por el tamaño exacto del bloque (10 píxeles)
    for x in range(0, ancho, tamano_bloque):
        pygame.draw.line(pantalla, gris_oscuro, (x, 0), (x, alto))
    
    # Dibuja líneas horizontales para completar la matriz/cuadrícula visual
    for y in range(0, alto, tamano_bloque):
        pygame.draw.line(pantalla, gris_oscuro, (0, y), (ancho, y))


def mostrar_puntuacion(puntos):
    # Renderiza el texto de los puntos en color amarillo 
    texto = fuente_puntos.render(f"Puntuación: {puntos}", True, amarillo)
    # Lo dibuja en la esquina superior izquierda (x:10, y:10)
    pantalla.blit(texto, [10, 10])


def mensaje(msg, color):
    # Renderiza un mensaje (como el de Game Over) 
    texto = fuente_mensajes.render(msg, True, color)
    # Lo centra de forma aproximada en la pantalla
    pantalla.blit(texto, [ancho / 6, alto / 3])


def loop_juego():
    # Bandera que indica si el programa debe cerrarse por completo
    game_over = False  
    # Bandera que activa la pantalla de "Perdiste" para decidir si reiniciar
    game_close = False 

    # Coordenadas iniciales de la serpiente (nace justo en el centro de la ventana)
    x1 = ancho / 2
    y1 = alto / 2

    # Variables que almacenan hacia dónde se está moviendo la serpiente en ese momento (0 = quieta)
    x1_cambio = 0
    y1_cambio = 0

    # Lista que guardará el historial de coordenadas (x, y) de todo el cuerpo de la serpiente
    serpiente_cuerpo = []
    # Inicia midiendo 1 solo bloque (la cabeza)
    largo_serpiente = 1 

    # Genera las coordenadas de la primera comida de forma aleatoria
    # Se asegura que se alinee a la cuadrícula (múltiplos de 10)
    comida_x = round(random.randrange(0, ancho - tamano_bloque) / 10.0) * 10.0
    comida_y = round(random.randrange(0, alto - tamano_bloque) / 10.0) * 10.0

    # Bucle principal: mantiene el juego corriendo constantemente
    while not game_over:
        
        # Bucle secundario: se activa únicamente cuando chocas y pierdes
        while game_close == True:
            # Limpia la pantalla dejándola completamente negra
            pantalla.fill(negro) 
            mensaje("¡Perdiste! Presiona C para Continuar o S para Salir", rojo)
            
            # Muestra tu puntuación final obtenida
            mostrar_puntuacion(largo_serpiente - 1) 
            
            # Refresca la pantalla para mostrar los textos
            pygame.display.update() 

            # Bucle de eventos para esperar a que el usuario presione S (salir) o C (continuar)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # Rompe el bucle principal y cierra el juego
                        game_over = True 
                        game_close = False
                    if event.key == pygame.K_c:
                        # Llama a la función recursivamente para reiniciar todo desde cero
                        loop_juego() 
        
        # Bucle de eventos principal: captura cada tecla o acción mientras juegas
        for event in pygame.event.get():
            # Si el usuario presiona la 'X' roja de la ventana de Windows
            if event.type == pygame.QUIT: 
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                # Direcciones de movimiento
                # Verificando que no vayas en la dirección opuesta (evita giros suicidas en 'U')
                if event.key == pygame.K_LEFT and x1_cambio == 0:
                    x1_cambio = -tamano_bloque
                    y1_cambio = 0
                elif event.key == pygame.K_RIGHT and x1_cambio == 0:
                    x1_cambio = tamano_bloque
                    y1_cambio = 0
                elif event.key == pygame.K_UP and y1_cambio == 0:
                    y1_cambio = -tamano_bloque
                    x1_cambio = 0
                elif event.key == pygame.K_DOWN and y1_cambio == 0:
                    y1_cambio = tamano_bloque
                    x1_cambio = 0

        # Sistema de colisiones con las paredes: si las coordenadas salen del tamaño de la ventana, mueres
        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            game_close = True

        # Actualiza las coordenadas actuales sumándoles el movimiento detectado en este fotograma
        x1 += x1_cambio
        y1 += y1_cambio

        # DIBUJADO EN CAPAS (De atrás hacia adelante):
        # 1. Pintamos el fondo negro para borrar el fotograma anterior por completo
        pantalla.fill(negro)
        
        # 2. Dibujamos nuestra cuadrícula de referencia encima del fondo
        dibujar_cuadricula()

        # 3. Dibujamos la comida (cuadrado verde) en sus coordenadas actuales
        pygame.draw.rect(pantalla, verde, [comida_x, comida_y, tamano_bloque, tamano_bloque])      

        # Actualizamos la posición de la cabeza de la serpiente
        cabeza_serpiente = []
        cabeza_serpiente.append(x1)
        cabeza_serpiente.append(y1)
        serpiente_cuerpo.append(cabeza_serpiente)

        # Ilusión de movimiento: Si la serpiente se movió pero no ha comido
        # Borramos la coordenada más vieja (la punta de la cola)
        if len(serpiente_cuerpo) > largo_serpiente:
            del serpiente_cuerpo[0]

        # Verificamos si la serpiente chocó consigo misma 
        # (si la cabeza tiene las mismas coordenadas que algún segmento de su cuerpo)
        for x in serpiente_cuerpo[:-1]:
            if x == cabeza_serpiente:
                game_close = True

        # 4. Dibujamos cada uno de los cuadrados blancos guardados en la lista (el cuerpo completo)
        for bloque in serpiente_cuerpo:
            pygame.draw.rect(pantalla, blanco, [bloque[0], bloque[1], tamano_bloque, tamano_bloque])

        # 5. Colocamos el contador de puntos siempre visible como la última capa encima de todo
        mostrar_puntuacion(largo_serpiente - 1)

        # Ejecutamos la proyección visual: le pedimos a Pygame que muestre todo lo que dibujamos en la pantalla
        pygame.display.update()

        # Lógica de puntuación y crecimiento: Si las coordenadas de la cabeza tocan exactamente a la comida...
        if x1 == comida_x and y1 == comida_y:
            # Generamos una comida nueva en un lugar aleatorio 
            comida_x = round(random.randrange(0, ancho - tamano_bloque) / 10.0) * 10.0
            comida_y = round(random.randrange(0, alto - tamano_bloque) / 10.0) * 10.0
            # Le sumamos +1 de tamaño a la serpiente
            largo_serpiente += 1

        # El reloj detiene el ciclo los milisegundos necesarios para asegurar que el juego corra a 15 fotogramas por segundo
        reloj.tick(velocidad)

    # Si el bucle principal se rompe (game_over = True), apagamos los motores de Pygame y salimos de Python
    pygame.quit()
    quit()


# Punto de entrada estándar para ejecutar el script
if __name__ == "__main__":
    loop_juego()