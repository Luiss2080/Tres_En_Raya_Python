import pygame
import math
from typing import Dict, List, Tuple
from datetime import datetime

from .sistema_navegacion import VentanaBase, TipoVentana, GestorVentanas

class VentanaTutorial(VentanaBase):
    """Ventana tutorial interactiva"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        self.pagina_actual = 0
        self.paginas_tutorial = [
            {
                'titulo': 'OBJETIVO DEL JUEGO',
                'contenido': [
                    'El objetivo es conseguir tres símbolos iguales',
                    'en línea: horizontal, vertical o diagonal.',
                    '',
                    'Tú juegas con X, la IA con O.',
                    'El primer jugador siempre eres tú.'
                ],
                'imagen': 'objetivo'
            },
            {
                'titulo': 'COMO JUGAR',
                'contenido': [
                    '1. Haz clic en cualquier casilla vacía',
                    '2. La IA jugará automáticamente después',
                    '3. Continúa hasta que alguien gane o empate',
                    '',
                    'La IA es invencible - usa algoritmo Minimax.',
                    'Lo mejor que puedes hacer es empatar.'
                ],
                'imagen': 'como_jugar'
            },
            {
                'titulo': 'CONTROLES',
                'contenido': [
                    'RATÓN: Clic para seleccionar casilla',
                    'ESC: Pausar juego o volver',
                    'R: Reiniciar partida actual',
                    'M: Volver al menú principal',
                    '',
                    'Disfruta del juego clásico',
                    'de Tres en Raya.'
                ],
                'imagen': 'controles'
            },
            {
                'titulo': 'ESTADÍSTICAS',
                'contenido': [
                    'El juego registra automáticamente:',
                    '• Partidas jugadas y resultados',
                    '• Racha actual y mejor racha',
                    '• Tiempo total de juego',
                    '• Historial de últimas 100 partidas',
                    '',
                    'Puedes resetear las estadísticas cuando quieras.'
                ],
                'imagen': 'estadisticas'
            }
        ]
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa controles del tutorial"""
        # Navegación
        self.agregar_boton('anterior', pygame.Rect(100, self.alto - 70, 120, 50), 
                          'ANTERIOR', self.pagina_anterior)
        
        self.agregar_boton('siguiente', pygame.Rect(250, self.alto - 70, 120, 50), 
                          'SIGUIENTE', self.pagina_siguiente)
        
        self.agregar_boton('salir_tutorial', pygame.Rect(400, self.alto - 70, 120, 50), 
                          'SALIR', self.salir_tutorial)
        
        self.agregar_boton('empezar', pygame.Rect(self.ancho - 170, self.alto - 70, 120, 50), 
                          'EMPEZAR', self.empezar_juego)
    
    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
    
    def pagina_siguiente(self):
        if self.pagina_actual < len(self.paginas_tutorial) - 1:
            self.pagina_actual += 1
    
    def salir_tutorial(self):
        self.gestor_ventanas.volver_atras()
    
    def empezar_juego(self):
        # Establecer configuración para modo clásico
        config = self.gestor_ventanas.obtener_configuracion()
        config.establecer('modo_actual', 'clasico')
        self.gestor_ventanas.cambiar_ventana(TipoVentana.JUEGO_CLASICO)
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza el tutorial"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        pagina = self.paginas_tutorial[self.pagina_actual]
        
        # Título principal
        fuente_titulo = self.gestor_ventanas.obtener_fuente('titulo')
        titulo = "TUTORIAL"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        titulo_rect = titulo_surface.get_rect(center=(self.ancho // 2, 50))
        pantalla.blit(titulo_surface, titulo_rect)
        
        # Panel de contenido
        panel_rect = pygame.Rect(100, 100, self.ancho - 200, 400)
        pygame.draw.rect(pantalla, tema['fondo_secundario'], panel_rect, border_radius=10)
        pygame.draw.rect(pantalla, tema['texto_secundario'], panel_rect, 2, border_radius=10)
        
        # Título de la página
        fuente_subtitulo = self.gestor_ventanas.obtener_fuente('subtitulo')
        pagina_titulo = pagina['titulo']
        pagina_titulo_surface = fuente_subtitulo.render(pagina_titulo, True, tema['texto_principal'])
        pagina_titulo_rect = pagina_titulo_surface.get_rect(center=(self.ancho // 2, 130))
        pantalla.blit(pagina_titulo_surface, pagina_titulo_rect)
        
        # Contenido de la página
        fuente_texto = self.gestor_ventanas.obtener_fuente('texto')
        y_contenido = 170
        
        for linea in pagina['contenido']:
            if linea.strip():  # Línea no vacía
                linea_surface = fuente_texto.render(linea, True, tema['texto_principal'])
                pantalla.blit(linea_surface, (130, y_contenido))
            y_contenido += 30
        
        # Indicador de página
        pagina_info = f"Página {self.pagina_actual + 1} de {len(self.paginas_tutorial)}"
        pagina_info_surface = fuente_texto.render(pagina_info, True, tema['texto_secundario'])
        pagina_info_rect = pagina_info_surface.get_rect(center=(self.ancho // 2, 470))
        pantalla.blit(pagina_info_surface, pagina_info_rect)
        
        # Dibujar una representación visual simple según la página
        self.dibujar_ilustracion_pagina(pantalla, pagina['imagen'])
        
        # Botones
        for boton in self.botones:
            # Habilitar/deshabilitar botones según página
            if boton['id'] == 'anterior':
                boton['color_normal'] = tema['texto_secundario'] if self.pagina_actual == 0 else tema['boton_normal']
            elif boton['id'] == 'siguiente':
                boton['color_normal'] = tema['texto_secundario'] if self.pagina_actual == len(self.paginas_tutorial) - 1 else tema['boton_normal']
            
            self.gestor_ventanas.renderizar_boton(pantalla, boton)
    
    def dibujar_ilustracion_pagina(self, pantalla: pygame.Surface, tipo_imagen: str):
        """Dibuja una ilustración simple para cada página"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        centro_x = self.ancho - 200
        centro_y = 250
        
        if tipo_imagen == 'objetivo':
            # Dibujar mini tablero con línea ganadora
            for i in range(4):
                pygame.draw.line(pantalla, tema['texto_secundario'], 
                               (centro_x - 30 + i * 20, centro_y - 30), 
                               (centro_x - 30 + i * 20, centro_y + 30), 2)
                pygame.draw.line(pantalla, tema['texto_secundario'], 
                               (centro_x - 30, centro_y - 30 + i * 20), 
                               (centro_x + 30, centro_y - 30 + i * 20), 2)
            
            # Símbolos X ganadores
            for i in range(3):
                x = centro_x - 20 + i * 20
                y = centro_y - 20
                pygame.draw.line(pantalla, tema['jugador_x'], (x-5, y-5), (x+5, y+5), 3)
                pygame.draw.line(pantalla, tema['jugador_x'], (x+5, y-5), (x-5, y+5), 3)
        
        elif tipo_imagen == 'como_jugar':
            # Dibujar cursor y tablero
            pygame.draw.circle(pantalla, tema['texto_principal'], (centro_x - 20, centro_y - 20), 8)
            pygame.draw.rect(pantalla, tema['tablero'], (centro_x - 10, centro_y - 10, 40, 40), border_radius=5)
            
        elif tipo_imagen == 'modos':
            # Iconos para diferentes modos
            pygame.draw.circle(pantalla, tema['boton_normal'], (centro_x, centro_y - 20), 15)  # Clásico
            pygame.draw.rect(pantalla, tema['ganador_highlight'], (centro_x - 15, centro_y, 30, 10))  # Cronómetro
            pygame.draw.polygon(pantalla, tema['empate'], [(centro_x, centro_y + 20), 
                                                          (centro_x - 10, centro_y + 30), 
                                                          (centro_x + 10, centro_y + 30)])  # Torneo


class VentanaHistorialPartidas(VentanaBase):
    """Ventana que muestra el historial de partidas"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        self.scroll_y = 0
        self.inicializar_ui()
    
    def inicializar_ui(self):
        self.agregar_boton('volver', pygame.Rect(50, self.alto - 70, 120, 50), 
                          'VOLVER', self.volver_estadisticas)
        
        self.agregar_boton('limpiar', pygame.Rect(self.ancho - 170, self.alto - 70, 120, 50), 
                          'LIMPIAR', self.limpiar_historial)
    
    def volver_estadisticas(self):
        self.gestor_ventanas.volver_atras()
    
    def limpiar_historial(self):
        stats = self.gestor_ventanas.obtener_estadisticas()
        stats.stats['historial_partidas'] = []
        stats.guardar_estadisticas()
    
    def manejar_tecla(self, tecla: int):
        """Maneja scroll con flechas"""
        if tecla == pygame.K_UP:
            self.scroll_y = max(0, self.scroll_y - 30)
        elif tecla == pygame.K_DOWN:
            self.scroll_y += 30
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza el historial de partidas"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        stats = self.gestor_ventanas.obtener_estadisticas()
        
        # Título
        fuente_titulo = self.gestor_ventanas.obtener_fuente('titulo')
        titulo = "HISTORIAL DE PARTIDAS"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        titulo_rect = titulo_surface.get_rect(center=(self.ancho // 2, 50))
        pantalla.blit(titulo_surface, titulo_rect)
        
        # Área de scroll
        area_scroll = pygame.Rect(50, 100, self.ancho - 100, 400)
        pygame.draw.rect(pantalla, tema['fondo_secundario'], area_scroll, border_radius=10)
        
        # Crear superficie para scroll
        superficie_scroll = pygame.Surface((area_scroll.width, 2000))
        superficie_scroll.fill(tema['fondo_secundario'])
        
        # Renderizar historial en la superficie de scroll
        fuente_texto = self.gestor_ventanas.obtener_fuente('pequeño')
        fuente_header = self.gestor_ventanas.obtener_fuente('texto')
        
        # Headers
        headers = ["FECHA", "RESULTADO", "MODO", "TIEMPO"]
        x_positions = [20, 150, 280, 400]
        
        for header, x_pos in zip(headers, x_positions):
            header_surface = fuente_header.render(header, True, tema['texto_principal'])
            superficie_scroll.blit(header_surface, (x_pos, 20))
        
        # Línea separadora
        pygame.draw.line(superficie_scroll, tema['texto_secundario'], 
                        (20, 45), (area_scroll.width - 40, 45), 2)
        
        # Partidas
        historial = stats.stats['historial_partidas']
        
        for i, partida in enumerate(reversed(historial[-50:])):  # Últimas 50 partidas
            y_pos = 60 + i * 30
            
            # Formatear fecha
            try:
                fecha_obj = datetime.fromisoformat(partida['fecha'])
                fecha_str = fecha_obj.strftime("%d/%m %H:%M")
            except:
                fecha_str = "N/A"
            
            # Color según resultado
            if partida['resultado'] == 'victoria':
                color = tema['jugador_x']
                resultado_text = "VICTORIA"
            elif partida['resultado'] == 'derrota':
                color = tema['jugador_o']
                resultado_text = "DERROTA"
            else:
                color = tema['empate']
                resultado_text = "EMPATE"
            
            # Renderizar información de la partida
            datos = [
                (fecha_str, tema['texto_secundario']),
                (resultado_text, color),
                (partida['modo'].upper(), tema['texto_secundario']),
                (f"{partida['tiempo']:.1f}s", tema['texto_secundario'])
            ]
            
            for (texto, color_texto), x_pos in zip(datos, x_positions):
                texto_surface = fuente_texto.render(texto, True, color_texto)
                superficie_scroll.blit(texto_surface, (x_pos, y_pos))
        
        # Aplicar scroll y blit a la pantalla principal
        pantalla.blit(superficie_scroll, area_scroll.topleft, 
                     (0, self.scroll_y, area_scroll.width, area_scroll.height))
        
        # Indicador de scroll si es necesario
        if len(historial) > 13:  # Más partidas de las que caben en pantalla
            fuente_pequena = self.gestor_ventanas.obtener_fuente('pequeño')
            scroll_info = "Usa las flechas para desplazarte"
            scroll_surface = fuente_pequena.render(scroll_info, True, tema['texto_secundario'])
            pantalla.blit(scroll_surface, (self.ancho // 2 - scroll_surface.get_width() // 2, 520))
        
        # Botones
        for boton in self.botones:
            self.gestor_ventanas.renderizar_boton(pantalla, boton)

class VentanaPausa(VentanaBase):
    """Ventana de pausa del juego"""
    
    def __init__(self, gestor_ventanas: GestorVentanas, ancho: int, alto: int):
        super().__init__(gestor_ventanas, ancho, alto)
        self.inicializar_ui()
    
    def inicializar_ui(self):
        centro_x = self.ancho // 2
        
        self.agregar_boton('continuar', pygame.Rect(centro_x - 100, 350, 200, 60), 
                          'CONTINUAR', self.continuar_juego)
        
        self.agregar_boton('reiniciar', pygame.Rect(centro_x - 100, 430, 200, 50), 
                          'REINICIAR', self.reiniciar_juego)
        
        self.agregar_boton('menu_principal', pygame.Rect(centro_x - 100, 510, 200, 50), 
                          'MENU PRINCIPAL', self.ir_menu_principal)
    
    def continuar_juego(self):
        self.gestor_ventanas.volver_atras()
    
    def reiniciar_juego(self):
        # Aquí se podría implementar lógica para reiniciar el juego actual
        self.gestor_ventanas.volver_atras()
    
    
    def ir_menu_principal(self):
        self.gestor_ventanas.cambiar_ventana(TipoVentana.MENU_PRINCIPAL)
    
    def manejar_tecla(self, tecla: int):
        """ESC para continuar"""
        if tecla == pygame.K_ESCAPE:
            self.continuar_juego()
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza la ventana de pausa"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        # Overlay semitransparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))
        
        # Panel central de pausa
        panel_rect = pygame.Rect(self.ancho // 2 - 150, 200, 300, 400)
        pygame.draw.rect(pantalla, tema['fondo_secundario'], panel_rect, border_radius=15)
        pygame.draw.rect(pantalla, tema['texto_principal'], panel_rect, 3, border_radius=15)
        
        # Título de pausa
        fuente_titulo = self.gestor_ventanas.obtener_fuente('titulo')
        titulo = "PAUSA"
        titulo_surface = fuente_titulo.render(titulo, True, tema['texto_principal'])
        titulo_rect = titulo_surface.get_rect(center=(self.ancho // 2, 250))
        pantalla.blit(titulo_surface, titulo_rect)
        
        # Botones
        for boton in self.botones:
            self.gestor_ventanas.renderizar_boton(pantalla, boton)
        
        # Instrucciones
        fuente_pequena = self.gestor_ventanas.obtener_fuente('pequeño')
        instruccion = "Presiona ESC para continuar"
        instruccion_surface = fuente_pequena.render(instruccion, True, tema['texto_secundario'])
        instruccion_rect = instruccion_surface.get_rect(center=(self.ancho // 2, 590))
        pantalla.blit(instruccion_surface, instruccion_rect)