import pygame
import time
import math
from typing import Dict, List, Tuple, Optional

from .sistema_navegacion import VentanaBase, TipoVentana, GestorVentanas
from .efectos_multimedia import GestorMultimedia
from logica.logica_tablero import TableroJuego
from logica.inteligencia_artificial import AlgoritmoMinimax

class VentanaJuegoBase(VentanaBase):
    """Clase base para todas las ventanas de juego"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        
        # Instancias de lógica
        self.tablero_juego = TableroJuego()
        self.algoritmo_minimax = AlgoritmoMinimax(self.tablero_juego)
        self.gestor_multimedia = GestorMultimedia()
        
        # Estado del juego
        self.juego_terminado = False
        self.ganador_actual = None
        self.linea_ganadora = None
        self.tiempo_inicio_partida = time.time()
        self.tiempo_fin_juego = 0
        self.movimientos_jugador = 0
        
        # Configuración del tablero visual
        self.configurar_tablero_visual()
        
        # UI común
        self.inicializar_ui_comun()
    
    def configurar_tablero_visual(self):
        """Configura las dimensiones y posiciones del tablero visual"""
        self.TAMANO_TABLERO = 480  # Aumentado de 400 a 480 para mejor visualización
        
        # Centrar el tablero verticalmente, dejando espacio para panel superior e inferior
        self.ESPACIO_SUPERIOR = 120  # Espacio para panel de información
        self.ESPACIO_INFERIOR = 100  # Espacio para botones
        
        self.inicio_tablero_x = (self.ancho - self.TAMANO_TABLERO) // 2
        self.inicio_tablero_y = self.ESPACIO_SUPERIOR + (self.alto - self.ESPACIO_SUPERIOR - self.ESPACIO_INFERIOR - self.TAMANO_TABLERO) // 2
        
        self.TAMANO_CELDA = self.TAMANO_TABLERO // 3
        self.GROSOR_LINEA = 4
        
        # Calcular posiciones de las celdas
        self.posiciones_celdas = []
        for fila in range(3):
            fila_posiciones = []
            for columna in range(3):
                x = self.inicio_tablero_x + columna * self.TAMANO_CELDA
                y = self.inicio_tablero_y + fila * self.TAMANO_CELDA
                fila_posiciones.append((x, y))
            self.posiciones_celdas.append(fila_posiciones)
    
    def inicializar_ui_comun(self):
        """Inicializa elementos UI comunes a todos los modos"""
        # Botones en la parte inferior, distribuidos horizontalmente
        y_botones = self.alto - 70  # 70px desde la parte inferior
        ancho_boton = 150
        alto_boton = 50
        
        # Calcular posiciones para centrar los 3 botones
        espacio_total = 3 * ancho_boton + 2 * 20  # 3 botones + 2 espacios de 20px
        x_inicio = (self.ancho - espacio_total) // 2
        
        self.agregar_boton('reiniciar', pygame.Rect(x_inicio, y_botones, ancho_boton, alto_boton), 
                          'REINICIAR', self.reiniciar_juego)
        
        self.agregar_boton('pausa', pygame.Rect(x_inicio + ancho_boton + 20, y_botones, ancho_boton, alto_boton), 
                          'PAUSA', self.pausar_juego)
        
        self.agregar_boton('menu', pygame.Rect(x_inicio + 2 * (ancho_boton + 20), y_botones, ancho_boton, alto_boton), 
                          'MENU', self.volver_menu)
    
    def manejar_clic(self, posicion: Tuple[int, int]):
        """Maneja clics del mouse"""
        # Primero verificar clics en botones
        super().manejar_clic(posicion)
        
        # Luego verificar clics en el tablero
        if not self.juego_terminado and self.tablero_juego.jugador_actual == 'X':
            self.manejar_clic_tablero(posicion)
    
    def manejar_clic_tablero(self, posicion: Tuple[int, int]):
        """Maneja clics en el tablero de juego"""
        x_mouse, y_mouse = posicion
        
        # Verificar si el clic está dentro del área del tablero
        if (self.inicio_tablero_x <= x_mouse <= self.inicio_tablero_x + self.TAMANO_TABLERO and
            self.inicio_tablero_y <= y_mouse <= self.inicio_tablero_y + self.TAMANO_TABLERO):
            
            # Calcular qué celda fue clickeada
            columna = (x_mouse - self.inicio_tablero_x) // self.TAMANO_CELDA
            fila = (y_mouse - self.inicio_tablero_y) // self.TAMANO_CELDA
            
            # Realizar movimiento del jugador humano
            if self.realizar_movimiento_humano(fila, columna):
                self.movimientos_jugador += 1
    
    def realizar_movimiento_humano(self, fila: int, columna: int) -> bool:
        """Realiza un movimiento del jugador humano"""
        if self.tablero_juego.realizar_movimiento(fila, columna, 'X'):
            # Efecto visual y sonoro
            x, y = self.posiciones_celdas[fila][columna]
            centro_x = x + self.TAMANO_CELDA // 2
            centro_y = y + self.TAMANO_CELDA // 2
            self.gestor_multimedia.procesar_evento_juego('simbolo_colocado', 
                                                       x=centro_x, y=centro_y, simbolo='X')
            
            # Verificar estado del juego
            if self.verificar_estado_juego():
                return True
            
            # Cambiar turno a la IA
            self.tablero_juego.jugador_actual = 'O'
            return True
        
        return False
    
    def ejecutar_movimiento_ia(self):
        """Ejecuta el movimiento de la IA"""
        if self.juego_terminado:
            return
        
        mejor_movimiento = self.algoritmo_minimax.obtener_mejor_movimiento_ia()
        
        if mejor_movimiento:
            fila, columna = mejor_movimiento
            self.tablero_juego.realizar_movimiento(fila, columna, 'O')
            
            # Efecto visual y sonoro
            x, y = self.posiciones_celdas[fila][columna]
            centro_x = x + self.TAMANO_CELDA // 2
            centro_y = y + self.TAMANO_CELDA // 2
            self.gestor_multimedia.procesar_evento_juego('simbolo_colocado', 
                                                       x=centro_x, y=centro_y, simbolo='O')
            
            # Verificar estado del juego
            self.verificar_estado_juego()
            
            # Cambiar turno al jugador humano
            self.tablero_juego.jugador_actual = 'X'
    
    def verificar_estado_juego(self) -> bool:
        """Verifica si el juego ha terminado"""
        ganador = self.tablero_juego.verificar_ganador()
        
        if ganador:
            self.juego_terminado = True
            self.ganador_actual = ganador
            self.tiempo_fin_juego = time.time()
            self.encontrar_linea_ganadora()
            
            # Registrar partida en estadísticas
            tiempo_jugado = self.tiempo_fin_juego - self.tiempo_inicio_partida
            resultado = 'victoria' if ganador == 'X' else 'derrota'
            
            stats = self.gestor_ventanas.obtener_estadisticas()
            config = self.gestor_ventanas.obtener_configuracion()
            modo = config.obtener('modo_actual', 'clasico')
            
            stats.registrar_partida(resultado, modo, tiempo_jugado, 
                                  self.movimientos_jugador, 'normal')
            
            # Efectos de victoria
            if self.linea_ganadora:
                self.procesar_efectos_victoria()
            
            return True
        
        elif self.tablero_juego.es_empate():
            self.juego_terminado = True
            self.ganador_actual = 'Empate'
            self.tiempo_fin_juego = time.time()
            
            # Registrar empate
            tiempo_jugado = self.tiempo_fin_juego - self.tiempo_inicio_partida
            stats = self.gestor_ventanas.obtener_estadisticas()
            config = self.gestor_ventanas.obtener_configuracion()
            modo = config.obtener('modo_actual', 'clasico')
            
            stats.registrar_partida('empate', modo, tiempo_jugado, 
                                  self.movimientos_jugador, 'normal')
            
            # Efecto de empate
            centro_x = self.inicio_tablero_x + self.TAMANO_TABLERO // 2
            centro_y = self.inicio_tablero_y + self.TAMANO_TABLERO // 2
            self.gestor_multimedia.procesar_evento_juego('empate', 
                                                       centro_x=centro_x, 
                                                       centro_y=centro_y)
            
            return True
        
        return False
    
    def encontrar_linea_ganadora(self):
        """Encuentra la línea ganadora para resaltarla"""
        if not self.ganador_actual or self.ganador_actual == 'Empate':
            return
        
        for combinacion in self.tablero_juego.todas_las_combinaciones_ganadoras:
            simbolos = [self.tablero_juego.matriz_tablero[fila][col] for fila, col in combinacion]
            if all(s == self.ganador_actual for s in simbolos):
                self.linea_ganadora = combinacion
                break
    
    def procesar_efectos_victoria(self):
        """Procesa efectos visuales de victoria"""
        if self.linea_ganadora:
            pos_inicio = self.linea_ganadora[0]
            pos_fin = self.linea_ganadora[2]
            
            x1, y1 = self.posiciones_celdas[pos_inicio[0]][pos_inicio[1]]
            x2, y2 = self.posiciones_celdas[pos_fin[0]][pos_fin[1]]
            
            x1 += self.TAMANO_CELDA // 2
            y1 += self.TAMANO_CELDA // 2
            x2 += self.TAMANO_CELDA // 2
            y2 += self.TAMANO_CELDA // 2
            
            self.gestor_multimedia.procesar_evento_juego('juego_ganado',
                                                       jugador=self.ganador_actual,
                                                       linea_coords=(x1, y1, x2, y2))
    
    def reiniciar_juego(self):
        """Reinicia el juego"""
        self.tablero_juego.reiniciar_tablero()
        self.juego_terminado = False
        self.ganador_actual = None
        self.linea_ganadora = None
        self.tiempo_inicio_partida = time.time()
        self.tiempo_fin_juego = 0
        self.movimientos_jugador = 0
        self.gestor_multimedia.limpiar()
        self.al_reiniciar_juego()
    
    def al_reiniciar_juego(self):
        """Método para override en subclases"""
        pass
    
    def pausar_juego(self):
        """Pausa el juego"""
        self.gestor_ventanas.cambiar_ventana(TipoVentana.PAUSA)
    
    def volver_menu(self):
        """Vuelve al menú principal"""
        self.gestor_ventanas.cambiar_ventana(TipoVentana.MENU_PRINCIPAL)
    
    
    def actualizar(self, dt: float):
        """Actualiza la lógica del juego"""
        # Actualizar efectos multimedia
        self.gestor_multimedia.actualizar()
        
        # Si es turno de la IA y el juego no ha terminado
        if (self.tablero_juego.jugador_actual == 'O' and 
            not self.juego_terminado):
            # Agregar pequeño delay para que se vea el movimiento
            if hasattr(self, '_tiempo_espera_ia'):
                if time.time() - self._tiempo_espera_ia > 0.8:
                    self.ejecutar_movimiento_ia()
                    delattr(self, '_tiempo_espera_ia')
            else:
                self._tiempo_espera_ia = time.time()
    
    def renderizar_tablero(self, pantalla: pygame.Surface):
        """Renderiza el tablero de juego"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Fondo del tablero
        tablero_rect = pygame.Rect(self.inicio_tablero_x - 10, self.inicio_tablero_y - 10, 
                                  self.TAMANO_TABLERO + 20, self.TAMANO_TABLERO + 20)
        pygame.draw.rect(pantalla, tema['tablero'], tablero_rect, border_radius=15)
        
        # Líneas del tablero
        self.dibujar_lineas_tablero(pantalla)
        
        # Símbolos del tablero
        self.dibujar_simbolos_tablero(pantalla)
        
        # Línea ganadora (si existe)
        if self.linea_ganadora:
            self.dibujar_linea_ganadora(pantalla)
    
    def dibujar_lineas_tablero(self, pantalla: pygame.Surface):
        """Dibuja las líneas del tablero"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Líneas verticales
        for i in range(1, 3):
            x = self.inicio_tablero_x + i * self.TAMANO_CELDA
            pygame.draw.line(pantalla, tema['lineas_tablero'], 
                           (x, self.inicio_tablero_y), 
                           (x, self.inicio_tablero_y + self.TAMANO_TABLERO), 
                           self.GROSOR_LINEA)
        
        # Líneas horizontales
        for i in range(1, 3):
            y = self.inicio_tablero_y + i * self.TAMANO_CELDA
            pygame.draw.line(pantalla, tema['lineas_tablero'],
                           (self.inicio_tablero_x, y),
                           (self.inicio_tablero_x + self.TAMANO_TABLERO, y),
                           self.GROSOR_LINEA)
    
    def dibujar_simbolos_tablero(self, pantalla: pygame.Surface):
        """Dibuja los símbolos X y O en el tablero"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        for fila in range(3):
            for columna in range(3):
                simbolo = self.tablero_juego.matriz_tablero[fila][columna]
                if simbolo != ' ':
                    x, y = self.posiciones_celdas[fila][columna]
                    centro_x = x + self.TAMANO_CELDA // 2
                    centro_y = y + self.TAMANO_CELDA // 2
                    
                    if simbolo == 'X':
                        self.dibujar_x(pantalla, centro_x, centro_y)
                    elif simbolo == 'O':
                        self.dibujar_o(pantalla, centro_x, centro_y)
    
    def dibujar_x(self, pantalla: pygame.Surface, centro_x: int, centro_y: int):
        """Dibuja el símbolo X"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        escala = self.gestor_multimedia.obtener_escala_simbolo(centro_x, centro_y)
        
        margen = int(35 * escala)
        color = tema['jugador_x']
        grosor = max(1, int(8 * escala))
        
        # Línea diagonal 1
        pygame.draw.line(pantalla, color,
                        (centro_x - margen, centro_y - margen),
                        (centro_x + margen, centro_y + margen), grosor)
        
        # Línea diagonal 2
        pygame.draw.line(pantalla, color,
                        (centro_x + margen, centro_y - margen),
                        (centro_x - margen, centro_y + margen), grosor)
    
    def dibujar_o(self, pantalla: pygame.Surface, centro_x: int, centro_y: int):
        """Dibuja el símbolo O"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        escala = self.gestor_multimedia.obtener_escala_simbolo(centro_x, centro_y)
        
        radio = max(1, int(40 * escala))
        color = tema['jugador_o']
        grosor = max(1, int(8 * escala))
        
        pygame.draw.circle(pantalla, color, (centro_x, centro_y), radio, grosor)
    
    def dibujar_linea_ganadora(self, pantalla: pygame.Surface):
        """Dibuja la línea que marca la combinación ganadora"""
        if not self.linea_ganadora:
            return
        
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Obtener posiciones de inicio y fin
        pos_inicio = self.linea_ganadora[0]
        pos_fin = self.linea_ganadora[2]
        
        # Calcular coordenadas en pantalla
        x1, y1 = self.posiciones_celdas[pos_inicio[0]][pos_inicio[1]]
        x2, y2 = self.posiciones_celdas[pos_fin[0]][pos_fin[1]]
        
        # Centrar en las celdas
        x1 += self.TAMANO_CELDA // 2
        y1 += self.TAMANO_CELDA // 2
        x2 += self.TAMANO_CELDA // 2
        y2 += self.TAMANO_CELDA // 2
        
        # Dibujar línea ganadora
        pygame.draw.line(pantalla, tema['ganador_highlight'], (x1, y1), (x2, y2), 12)

class VentanaJuegoClasico(VentanaJuegoBase):
    """Modo de juego clásico sin límite de tiempo"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza el modo de juego clásico"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Panel de información
        self.renderizar_panel_info(pantalla)
        
        # Tablero principal
        self.renderizar_tablero(pantalla)
        
        # Estado del juego
        self.renderizar_estado_juego(pantalla)
        
        # Efectos visuales
        self.gestor_multimedia.dibujar(pantalla)
        
        # Botones
        for boton in self.botones:
            self.gestor_ventanas.renderizar_boton(pantalla, boton)
    
    def renderizar_panel_info(self, pantalla: pygame.Surface):
        """Renderiza el panel de información en la parte superior"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Fondo del panel horizontal en la parte superior
        panel_rect = pygame.Rect(20, 20, self.ancho - 40, 80)
        pygame.draw.rect(pantalla, tema['fondo_secundario'], panel_rect, border_radius=10)
        pygame.draw.rect(pantalla, tema['texto_secundario'], panel_rect, 2, border_radius=10)
        
        # Fuentes
        fuente_titulo = self.gestor_ventanas.obtener_fuente('subtitulo')
        fuente_texto = self.gestor_ventanas.obtener_fuente('texto')
        
        # Título del modo (izquierda)
        titulo = "MODO CLASICO"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        pantalla.blit(titulo_surface, (40, 35))
        
        # Información de jugadores (centro-izquierda)
        info_humano = "Tu: X"
        info_ia = "IA: O"
        
        humano_surface = fuente_texto.render(info_humano, True, tema['jugador_x'])
        ia_surface = fuente_texto.render(info_ia, True, tema['jugador_o'])
        
        x_jugadores = 250
        pantalla.blit(humano_surface, (x_jugadores, 40))
        pantalla.blit(ia_surface, (x_jugadores, 65))
        
        # Estadísticas rápidas (centro-derecha)
        stats = self.gestor_ventanas.obtener_estadisticas()
        x_stats_base = 400
        
        # Primera fila de estadísticas
        stat1 = f"Partidas: {stats.stats['partidas_jugadas']}"
        stat2 = f"Victorias: {stats.stats['victorias']}"
        
        stat1_surface = fuente_texto.render(stat1, True, tema['texto_secundario'])
        stat2_surface = fuente_texto.render(stat2, True, tema['texto_secundario'])
        
        pantalla.blit(stat1_surface, (x_stats_base, 40))
        pantalla.blit(stat2_surface, (x_stats_base + 150, 40))
        
        # Segunda fila de estadísticas
        stat3 = f"Racha: {stats.stats['racha_actual']}"
        stat3_surface = fuente_texto.render(stat3, True, tema['texto_secundario'])
        pantalla.blit(stat3_surface, (x_stats_base, 65))
    
    def renderizar_estado_juego(self, pantalla: pygame.Surface):
        """Renderiza el estado actual del juego"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        fuente_estado = self.gestor_ventanas.obtener_fuente('subtitulo')
        
        # Posicionar el texto de estado debajo del tablero, antes de los botones
        y_estado = self.inicio_tablero_y + self.TAMANO_TABLERO + 20
        
        if self.juego_terminado:
            if self.ganador_actual == 'Empate':
                texto_estado = "EMPATE - Buen juego!"
                color_estado = tema['empate']
            elif self.ganador_actual == 'X':
                texto_estado = "¡FELICIDADES! ¡HAS GANADO!"
                color_estado = tema['jugador_x']
            else:
                texto_estado = "La IA ha ganado esta ronda"
                color_estado = tema['jugador_o']
        else:
            if self.tablero_juego.jugador_actual == 'X':
                texto_estado = "Tu turno - Haz clic en una casilla"
                color_estado = tema['jugador_x']
            else:
                texto_estado = "IA está calculando..."
                color_estado = tema['jugador_o']
        
        # Renderizar texto del estado centrado
        superficie_texto = fuente_estado.render(texto_estado, True, color_estado)
        rect_texto = superficie_texto.get_rect(center=(self.ancho//2, y_estado))
        pantalla.blit(superficie_texto, rect_texto)


