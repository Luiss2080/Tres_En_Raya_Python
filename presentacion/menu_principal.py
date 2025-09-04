import pygame
import math
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from .sistema_navegacion import VentanaBase, TipoVentana, GestorVentanas
from logica.logica_tablero import TableroJuego
from logica.inteligencia_artificial import AlgoritmoMinimax

class VentanaMenuPrincipal(VentanaBase):
    """Ventana del menú principal mejorada"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        self.tiempo_animacion = 0
        self.particulas_fondo = []
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa la interfaz de usuario"""
        centro_x = self.ancho // 2
        
        # Botones principales
        self.agregar_boton('jugar', pygame.Rect(centro_x - 120, 300, 240, 60), 
                          'JUGAR', self.ir_a_juego_clasico)
        
        self.agregar_boton('estadisticas', pygame.Rect(centro_x - 120, 400, 240, 50), 
                          'ESTADISTICAS', self.ir_a_estadisticas)
        
        self.agregar_boton('tutorial', pygame.Rect(centro_x - 120, 480, 240, 50), 
                          'TUTORIAL', self.ir_a_tutorial)
        
        self.agregar_boton('salir', pygame.Rect(centro_x - 60, 560, 120, 40), 
                          'SALIR', self.salir_juego)
        
        # Inicializar partículas de fondo
        self.crear_particulas_fondo()
    
    def crear_particulas_fondo(self):
        """Crea partículas decorativas para el fondo"""
        import random
        for _ in range(50):
            self.particulas_fondo.append({
                'x': random.randint(0, self.ancho),
                'y': random.randint(0, self.alto),
                'velocidad': random.uniform(10, 30),
                'tamaño': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            })
    
    def ir_a_juego_clasico(self):
        # Establecer configuración para modo clásico
        config = self.gestor_ventanas.obtener_configuracion()
        config.establecer('modo_actual', 'clasico')
        self.gestor_ventanas.cambiar_ventana(TipoVentana.JUEGO_CLASICO)
    
    def ir_a_estadisticas(self):
        self.gestor_ventanas.cambiar_ventana(TipoVentana.ESTADISTICAS)
    
    
    def ir_a_tutorial(self):
        self.gestor_ventanas.cambiar_ventana(TipoVentana.TUTORIAL)
    
    
    def salir_juego(self):
        pygame.quit()
        exit()
    
    def actualizar(self, dt: float):
        """Actualiza animaciones"""
        self.tiempo_animacion += dt
        
        # Actualizar partículas de fondo
        for particula in self.particulas_fondo:
            particula['y'] += particula['velocidad'] * dt
            if particula['y'] > self.alto + 10:
                particula['y'] = -10
                particula['x'] = __import__('random').randint(0, self.ancho)
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza la ventana del menú principal"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Renderizar partículas de fondo
        for particula in self.particulas_fondo:
            s = pygame.Surface((particula['tamaño'] * 2, particula['tamaño'] * 2))
            s.set_alpha(particula['alpha'])
            s.fill(tema['texto_secundario'])
            pantalla.blit(s, (int(particula['x']), int(particula['y'])))
        
        # Título principal con animación
        fuente_titulo = self.gestor_ventanas.obtener_fuente('titulo')
        escala_titulo = 1.0 + 0.1 * math.sin(self.tiempo_animacion * 2)
        
        titulo = "TRES EN RAYA"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        titulo_escalado = pygame.transform.scale(titulo_surface, 
                                                (int(titulo_surface.get_width() * escala_titulo),
                                                 int(titulo_surface.get_height() * escala_titulo)))
        
        titulo_rect = titulo_escalado.get_rect(center=(self.ancho // 2, 120))
        pantalla.blit(titulo_escalado, titulo_rect)
        
        # Subtítulo
        fuente_subtitulo = self.gestor_ventanas.obtener_fuente('subtitulo')
        subtitulo = "Algoritmo Minimax • IA Invencible"
        subtitulo_surface = fuente_subtitulo.render(subtitulo, True, tema['texto_secundario'])
        subtitulo_rect = subtitulo_surface.get_rect(center=(self.ancho // 2, 180))
        pantalla.blit(subtitulo_surface, subtitulo_rect)
        
        # Renderizar botones
        for boton in self.botones:
            self.gestor_ventanas.renderizar_boton(pantalla, boton)
        
        # Información de versión
        fuente_pequeña = self.gestor_ventanas.obtener_fuente('pequeño')
        version_text = "v2.0 - Pygame Edition"
        version_surface = fuente_pequeña.render(version_text, True, tema['texto_secundario'])
        pantalla.blit(version_surface, (10, self.alto - 25))


class VentanaEstadisticas(VentanaBase):
    """Ventana que muestra las estadísticas del jugador"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa la interfaz de estadísticas"""
        # Botón volver
        self.agregar_boton('volver', pygame.Rect(50, self.alto - 70, 120, 50), 
                          'VOLVER', self.volver_menu)
        
        # Botón resetear estadísticas
        self.agregar_boton('reset', pygame.Rect(self.ancho - 200, self.alto - 70, 150, 50), 
                          'RESETEAR', self.resetear_stats)
        
        # Botón historial
        self.agregar_boton('historial', pygame.Rect(self.ancho // 2 - 75, self.alto - 70, 150, 50), 
                          'HISTORIAL', self.ver_historial)
    
    def volver_menu(self):
        self.gestor_ventanas.volver_atras()
    
    def resetear_stats(self):
        stats = self.gestor_ventanas.obtener_estadisticas()
        stats.resetear_estadisticas()
    
    def ver_historial(self):
        self.gestor_ventanas.cambiar_ventana(TipoVentana.HISTORIAL_PARTIDAS)
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza la ventana de estadísticas"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        stats = self.gestor_ventanas.obtener_estadisticas()
        
        # Título
        fuente_titulo = self.gestor_ventanas.obtener_fuente('titulo')
        titulo = "ESTADISTICAS"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        titulo_rect = titulo_surface.get_rect(center=(self.ancho // 2, 50))
        pantalla.blit(titulo_surface, titulo_rect)
        
        # Panel de estadísticas principales
        panel_rect = pygame.Rect(50, 100, self.ancho - 100, 400)
        pygame.draw.rect(pantalla, tema['fondo_secundario'], panel_rect, border_radius=10)
        pygame.draw.rect(pantalla, tema['texto_secundario'], panel_rect, 2, border_radius=10)
        
        # Estadísticas
        fuente_texto = self.gestor_ventanas.obtener_fuente('texto')
        fuente_numero = self.gestor_ventanas.obtener_fuente('subtitulo')
        
        y_pos = 130
        estadisticas_info = [
            ("Partidas Jugadas", str(stats.stats['partidas_jugadas'])),
            ("Victorias", str(stats.stats['victorias'])),
            ("Derrotas", str(stats.stats['derrotas'])),
            ("Empates", str(stats.stats['empates'])),
            ("Porcentaje de Victoria", f"{stats.obtener_porcentaje_victoria():.1f}%"),
            ("Racha Actual", str(stats.stats['racha_actual'])),
            ("Mejor Racha", str(stats.stats['mejor_racha'])),
            ("Tiempo Total", f"{stats.stats['tiempo_total_jugado']//60:.0f} min"),
        ]
        
        for i, (label, valor) in enumerate(estadisticas_info):
            if i % 2 == 0:  # Columna izquierda
                x_label = 80
                x_valor = 300
            else:  # Columna derecha
                x_label = 450
                x_valor = 670
                
            if i % 2 == 0:
                y_actual = y_pos
            else:
                y_actual = y_pos
                y_pos += 40
            
            # Etiqueta
            label_surface = fuente_texto.render(label, True, tema['texto_secundario'])
            pantalla.blit(label_surface, (x_label, y_actual))
            
            # Valor
            valor_surface = fuente_numero.render(valor, True, tema['texto_principal'])
            pantalla.blit(valor_surface, (x_valor, y_actual - 5))
        
        # Renderizar botones
        for boton in self.botones:
            self.gestor_ventanas.renderizar_boton(pantalla, boton)


