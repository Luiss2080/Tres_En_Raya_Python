import pygame
import sys
import os
from typing import Optional

# Agregar la carpeta padre al path para importar lógica
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .sistema_navegacion import GestorVentanas, TipoVentana
from .menu_principal import (VentanaMenuPrincipal, VentanaEstadisticas)
from .juego_clasico import VentanaJuegoClasico
from .ventanas_auxiliares import VentanaTutorial, VentanaHistorialPartidas, VentanaPausa

class MotorJuegoAvanzado:
    """Motor principal del juego con sistema completo de ventanas"""
    
    def __init__(self):
        # Inicializar pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=512)
        
        # Configuración inicial de ventana
        self.ANCHO_VENTANA = 900
        self.ALTO_VENTANA = 700
        self.pantalla = pygame.display.set_mode((self.ANCHO_VENTANA, self.ALTO_VENTANA))
        pygame.display.set_caption("Tres en Raya - Edicion Avanzada")
        
        # Configurar icono si existe
        self.configurar_icono()
        
        # Control de tiempo
        self.reloj = pygame.time.Clock()
        self.FPS = 60
        self.ejecutando = True
        
        # Sistemas principales
        self.gestor_ventanas = GestorVentanas(self.ANCHO_VENTANA, self.ALTO_VENTANA)
        
        # Variables de rendimiento
        self.mostrar_fps = False
        self.tiempo_delta = 0
        self.frames_por_segundo = 0
        
        # Configurar FPS después de inicializar gestor_ventanas
        self.configurar_fps()
        
        # Registrar todas las ventanas
        self.registrar_ventanas()
        
        # Inicializar en menú principal
        self.gestor_ventanas.cambiar_ventana(TipoVentana.MENU_PRINCIPAL, agregar_a_pila=False)
        
    
    def configurar_icono(self):
        """Configura el icono de la ventana"""
        try:
            # Crear un icono simple usando pygame
            icono = pygame.Surface((32, 32))
            icono.fill((26, 35, 46))  # Color de fondo
            
            # Dibujar una X y O pequeñas
            pygame.draw.line(icono, (52, 152, 219), (5, 5), (15, 15), 2)  # X azul
            pygame.draw.line(icono, (52, 152, 219), (15, 5), (5, 15), 2)
            pygame.draw.circle(icono, (231, 76, 60), (24, 8), 6, 2)  # O rojo
            
            pygame.display.set_icon(icono)
        except Exception as e:
            print(f"No se pudo configurar icono: {e}")
    
    def configurar_fps(self):
        """Configura FPS basado en la configuración"""
        config = self.gestor_ventanas.obtener_configuracion()
        self.mostrar_fps = config.obtener('mostrar_fps', False)
        fps_objetivo = config.obtener('fps_objetivo', 60)
        self.FPS = max(30, min(120, fps_objetivo))
    
    def registrar_ventanas(self):
        """Registra todas las ventanas del juego"""
        # Ventanas principales
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.MENU_PRINCIPAL,
            VentanaMenuPrincipal(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
        
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.ESTADISTICAS,
            VentanaEstadisticas(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
        
        # Ventanas de juego
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.JUEGO_CLASICO,
            VentanaJuegoClasico(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
        
        
        # Ventanas extras
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.TUTORIAL,
            VentanaTutorial(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
        
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.HISTORIAL_PARTIDAS,
            VentanaHistorialPartidas(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
        
        self.gestor_ventanas.registrar_ventana(
            TipoVentana.PAUSA,
            VentanaPausa(self.gestor_ventanas, self.ANCHO_VENTANA, self.ALTO_VENTANA)
        )
    
    def manejar_eventos(self):
        """Maneja todos los eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                self.manejar_tecla_global(evento.key)
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pass
            
            elif evento.type == pygame.MOUSEMOTION:
                # Detectar hover en botones para sonido
                self.manejar_hover_audio(evento.pos)
            
            # Pasar evento al gestor de ventanas
            self.gestor_ventanas.manejar_evento(evento)
    
    def manejar_tecla_global(self, tecla: int):
        """Maneja teclas globales del sistema"""
        if tecla == pygame.K_F11:
            # Alternar pantalla completa
            self.alternar_pantalla_completa()
        elif tecla == pygame.K_F3:
            # Alternar mostrar FPS
            self.mostrar_fps = not self.mostrar_fps
            config = self.gestor_ventanas.obtener_configuracion()
            config.establecer('mostrar_fps', self.mostrar_fps)
        elif tecla == pygame.K_F1:
            # Ir a tutorial rápidamente
            self.gestor_ventanas.cambiar_ventana(TipoVentana.TUTORIAL)
        elif tecla == pygame.K_ESCAPE:
            # ESC global - comportamiento según contexto
            ventana_actual = self.gestor_ventanas.ventana_actual
            if ventana_actual == TipoVentana.JUEGO_CLASICO:
                self.gestor_ventanas.cambiar_ventana(TipoVentana.PAUSA)
            elif ventana_actual != TipoVentana.MENU_PRINCIPAL:
                self.gestor_ventanas.volver_atras()
    
    def manejar_hover_audio(self, pos_mouse):
        """Maneja audio de hover en botones"""
        # Esta es una implementación básica - se podría mejorar
        # detectando específicamente cuándo se entra en un botón por primera vez
        pass
    
    def alternar_pantalla_completa(self):
        """Alterna entre pantalla completa y ventana"""
        config = self.gestor_ventanas.obtener_configuracion()
        pantalla_completa = config.obtener('pantalla_completa', False)
        
        if pantalla_completa:
            self.pantalla = pygame.display.set_mode((self.ANCHO_VENTANA, self.ALTO_VENTANA))
        else:
            self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        config.establecer('pantalla_completa', not pantalla_completa)
    
    def actualizar(self):
        """Actualiza toda la lógica del juego"""
        # Calcular delta time
        self.tiempo_delta = self.reloj.tick(self.FPS) / 1000.0
        self.frames_por_segundo = self.reloj.get_fps()
        
        # Actualizar gestor de ventanas
        self.gestor_ventanas.actualizar(self.tiempo_delta)
        
    
    
    def renderizar(self):
        """Renderiza todo el contenido visual"""
        # Renderizar ventana actual
        self.gestor_ventanas.renderizar(self.pantalla)
        
        # Mostrar información de debug si está habilitada
        if self.mostrar_fps:
            self.renderizar_info_debug()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def renderizar_info_debug(self):
        """Renderiza información de debug (FPS, memoria, etc.)"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        fuente_debug = self.gestor_ventanas.obtener_fuente('pequeño')
        
        # Información de rendimiento
        fps_text = f"FPS: {self.frames_por_segundo:.1f}"
        dt_text = f"DT: {self.tiempo_delta*1000:.1f}ms"
        
        # Información simplificada
        audio_text = "Audio: Deshabilitado"
        
        # Información de memoria (aproximada)
        ventanas_text = f"Ventanas: {len(self.gestor_ventanas.ventanas)}"
        
        debug_lines = [fps_text, dt_text, audio_text, ventanas_text]
        
        # Renderizar en la esquina superior derecha
        for i, line in enumerate(debug_lines):
            text_surface = fuente_debug.render(line, True, tema['texto_secundario'])
            x = self.ANCHO_VENTANA - text_surface.get_width() - 10
            y = 10 + i * 20
            self.pantalla.blit(text_surface, (x, y))
    
    def cleanup(self):
        """Limpieza antes de cerrar el juego"""
        print("Guardando configuraciones...")
        
        # Guardar configuración final
        self.gestor_ventanas.obtener_configuracion().guardar_configuracion()
        
        
        # Cleanup de pygame
        pygame.mixer.quit()
        pygame.quit()
    
    def ejecutar(self):
        """Bucle principal del juego"""
        print("Iniciando Tres en Raya - Edicion Avanzada")
        print("Motor de juego cargado exitosamente")
        print("Sistema de ventanas inicializado")
        print("Sistema de audio configurado")
        print("Listo para jugar!")
        
        try:
            while self.ejecutando:
                # Manejar eventos
                self.manejar_eventos()
                
                # Actualizar lógica
                self.actualizar()
                
                # Renderizar
                self.renderizar()
            
        except KeyboardInterrupt:
            print("\nJuego interrumpido por el usuario")
        except Exception as e:
            print(f"ERROR critico: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            self.cleanup()
            print("Gracias por jugar!")

def main():
    """Función principal"""
    try:
        motor = MotorJuegoAvanzado()
        motor.ejecutar()
    except Exception as e:
        print(f"ERROR fatal al inicializar: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())