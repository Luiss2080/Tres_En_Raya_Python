import pygame
import sys
import os
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
import json
from datetime import datetime, date

# Agregar la carpeta padre al path para importar lógica
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TipoVentana(Enum):
    MENU_PRINCIPAL = "menu_principal"
    ESTADISTICAS = "estadisticas"
    JUEGO_CLASICO = "juego_clasico"
    TUTORIAL = "tutorial"
    HISTORIAL_PARTIDAS = "historial_partidas"
    PAUSA = "pausa"

class Tema:
    """Tema visual único para el juego"""
    
    COLORES = {
        'fondo_principal': (26, 35, 46),
        'fondo_secundario': (52, 73, 94),
        'tablero': (236, 240, 241),
        'lineas_tablero': (52, 73, 94),
        'jugador_x': (52, 152, 219),
        'jugador_o': (231, 76, 60),
        'texto_principal': (236, 240, 241),
        'texto_secundario': (149, 165, 166),
        'boton_normal': (46, 204, 113),
        'boton_hover': (39, 174, 96),
        'ganador_highlight': (241, 196, 15),
        'empate': (155, 89, 182)
    }

class GestorEstadisticas:
    """Gestiona las estadísticas del jugador"""
    
    def __init__(self):
        self.archivo_datos = "datos_juego.json"
        self.stats = self.cargar_estadisticas()
    
    def cargar_estadisticas(self) -> Dict[str, Any]:
        """Carga estadísticas desde archivo"""
        # Estadísticas por defecto
        stats_default = {
            'partidas_jugadas': 0,
            'victorias': 0,
            'derrotas': 0,
            'empates': 0,
            'tiempo_total_jugado': 0,  # en segundos
            'mejor_tiempo_victoria': float('inf'),
            'racha_actual': 0,
            'mejor_racha': 0,
            'primer_juego': None,
            'ultimo_juego': None,
            'modos_jugados': {},
            'dificultades_vencidas': {},
            'historial_partidas': []
        }
        
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    # Si los datos tienen la estructura anidada, extraer solo las estadísticas
                    if 'estadisticas' in datos:
                        stats_cargadas = datos['estadisticas']
                    else:
                        stats_cargadas = datos
                    
                    # Combinar estadísticas cargadas con las por defecto para evitar KeyError
                    for key, value in stats_cargadas.items():
                        if key in stats_default:
                            stats_default[key] = value
                    
                    return stats_default
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
        
        return stats_default
    
    def guardar_estadisticas(self):
        """Guarda estadísticas a archivo"""
        try:
            # Cargar configuración existente si existe
            datos_completos = {}
            if os.path.exists(self.archivo_datos):
                try:
                    with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                        datos_completos = json.load(f)
                except:
                    pass
            
            # Actualizar solo la sección de estadísticas
            datos_completos['estadisticas'] = self.stats
            
            # Mantener configuración por defecto si no existe
            if 'configuracion' not in datos_completos:
                datos_completos['configuracion'] = {
                    'fps_objetivo': 60
                }
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")
    
    def registrar_partida(self, resultado: str, modo: str, tiempo_jugado: float, 
                         movimientos: int = 0, ia_nivel: str = "normal"):
        """Registra una nueva partida"""
        self.stats['partidas_jugadas'] += 1
        self.stats['tiempo_total_jugado'] += tiempo_jugado
        
        # Actualizar fechas
        ahora = datetime.now().isoformat()
        if not self.stats['primer_juego']:
            self.stats['primer_juego'] = ahora
        self.stats['ultimo_juego'] = ahora
        
        # Registrar resultado
        if resultado == 'victoria':
            self.stats['victorias'] += 1
            self.stats['racha_actual'] += 1
            self.stats['mejor_racha'] = max(self.stats['mejor_racha'], self.stats['racha_actual'])
            if tiempo_jugado < self.stats['mejor_tiempo_victoria']:
                self.stats['mejor_tiempo_victoria'] = tiempo_jugado
        elif resultado == 'derrota':
            self.stats['derrotas'] += 1
            self.stats['racha_actual'] = 0
        else:  # empate
            self.stats['empates'] += 1
            # Los empates no rompen la racha pero tampoco la aumentan
        
        # Registrar modo de juego
        if modo not in self.stats['modos_jugados']:
            self.stats['modos_jugados'][modo] = 0
        self.stats['modos_jugados'][modo] += 1
        
        # Registrar dificultad vencida
        if resultado == 'victoria':
            if ia_nivel not in self.stats['dificultades_vencidas']:
                self.stats['dificultades_vencidas'][ia_nivel] = 0
            self.stats['dificultades_vencidas'][ia_nivel] += 1
        
        # Agregar al historial (mantener solo últimas 100 partidas)
        partida_info = {
            'fecha': ahora,
            'resultado': resultado,
            'modo': modo,
            'tiempo': tiempo_jugado,
            'movimientos': movimientos,
            'ia_nivel': ia_nivel
        }
        self.stats['historial_partidas'].append(partida_info)
        if len(self.stats['historial_partidas']) > 100:
            self.stats['historial_partidas'] = self.stats['historial_partidas'][-100:]
        
        self.guardar_estadisticas()
    
    def obtener_porcentaje_victoria(self) -> float:
        """Calcula el porcentaje de victorias"""
        total = self.stats['partidas_jugadas']
        if total == 0:
            return 0.0
        return (self.stats['victorias'] / total) * 100
    
    def obtener_tiempo_promedio(self) -> float:
        """Calcula el tiempo promedio por partida"""
        if self.stats['partidas_jugadas'] == 0:
            return 0.0
        return self.stats['tiempo_total_jugado'] / self.stats['partidas_jugadas']
    
    def resetear_estadisticas(self):
        """Resetea todas las estadísticas"""
        self.stats = {
            'partidas_jugadas': 0,
            'victorias': 0,
            'derrotas': 0,
            'empates': 0,
            'tiempo_total_jugado': 0,
            'mejor_tiempo_victoria': float('inf'),
            'racha_actual': 0,
            'mejor_racha': 0,
            'primer_juego': None,
            'ultimo_juego': None,
            'modos_jugados': {},
            'dificultades_vencidas': {},
            'historial_partidas': []
        }
        self.guardar_estadisticas()

class GestorConfiguracion:
    """Gestiona las configuraciones del juego"""
    
    def __init__(self):
        self.archivo_config = "configuracion_juego.json"
        self.config = self.cargar_configuracion()
    
    def cargar_configuracion(self) -> Dict[str, Any]:
        """Carga configuración desde archivo"""
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
        
        # Configuración por defecto
        return {
            'fps_objetivo': 60,
            'mostrar_fps': False,
            'auto_guardar': True,
            'modo_actual': 'clasico'
        }
    
    def guardar_configuracion(self):
        """Guarda configuración a archivo"""
        try:
            with open(self.archivo_config, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def obtener(self, clave: str, valor_defecto=None):
        """Obtiene un valor de configuración"""
        return self.config.get(clave, valor_defecto)
    
    def establecer(self, clave: str, valor: Any):
        """Establece un valor de configuración"""
        self.config[clave] = valor
        if self.config.get('auto_guardar', True):
            self.guardar_configuracion()

class VentanaBase:
    """Clase base para todas las ventanas del juego"""
    
    def __init__(self, gestor_ventanas, ancho: int, alto: int):
        self.gestor_ventanas = gestor_ventanas
        self.ancho = ancho
        self.alto = alto
        self.activa = False
        self.botones: List[Dict] = []
        self.elementos_ui: List[Dict] = []
        
    def activar(self):
        """Activa la ventana"""
        self.activa = True
        self.al_activar()
    
    def desactivar(self):
        """Desactiva la ventana"""
        self.activa = False
        self.al_desactivar()
    
    def al_activar(self):
        """Llamado cuando la ventana se activa"""
        pass
    
    def al_desactivar(self):
        """Llamado cuando la ventana se desactiva"""
        pass
    
    def manejar_evento(self, evento: pygame.event.Event):
        """Maneja eventos de pygame"""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.manejar_clic(evento.pos)
        elif evento.type == pygame.KEYDOWN:
            self.manejar_tecla(evento.key)
        elif evento.type == pygame.MOUSEMOTION:
            self.manejar_mouse_movimiento(evento.pos)
    
    def manejar_clic(self, posicion: Tuple[int, int]):
        """Maneja clics del mouse"""
        for boton in self.botones:
            if boton['rect'].collidepoint(posicion):
                if 'accion' in boton:
                    boton['accion']()
                self.al_hacer_clic_boton(boton['id'])
                break
    
    def manejar_tecla(self, tecla: int):
        """Maneja teclas presionadas"""
        pass
    
    def manejar_mouse_movimiento(self, posicion: Tuple[int, int]):
        """Maneja movimiento del mouse para efectos hover"""
        for boton in self.botones:
            boton['hover'] = boton['rect'].collidepoint(posicion)
    
    def al_hacer_clic_boton(self, boton_id: str):
        """Llamado cuando se hace clic en un botón"""
        pass
    
    def actualizar(self, dt: float):
        """Actualiza la lógica de la ventana"""
        pass
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza la ventana"""
        pass
    
    def agregar_boton(self, boton_id: str, rect: pygame.Rect, texto: str, 
                     accion=None, color_normal=None, color_hover=None):
        """Agrega un botón a la ventana"""
        tema = self.gestor_ventanas.obtener_tema_actual()
        
        boton = {
            'id': boton_id,
            'rect': rect,
            'texto': texto,
            'accion': accion,
            'color_normal': color_normal or tema['boton_normal'],
            'color_hover': color_hover or tema['boton_hover'],
            'hover': False
        }
        
        self.botones.append(boton)
        return boton

class GestorVentanas:
    """Gestor principal que maneja todas las ventanas del juego"""
    
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self.ventanas: Dict[TipoVentana, VentanaBase] = {}
        self.ventana_actual: Optional[TipoVentana] = None
        self.pila_ventanas: List[TipoVentana] = []  # Para navegación hacia atrás
        
        # Gestores auxiliares
        self.gestor_datos = GestorEstadisticas()
        self.gestor_config = GestorConfiguracion()
        
        
        # Fuentes
        self.cargar_fuentes()
    
    def cargar_fuentes(self):
        """Carga las fuentes del juego"""
        try:
            self.fuentes = {
                'titulo': pygame.font.Font(None, 48),
                'subtitulo': pygame.font.Font(None, 32),
                'boton': pygame.font.Font(None, 28),
                'texto': pygame.font.Font(None, 24),
                'pequeño': pygame.font.Font(None, 20)
            }
        except:
            # Fallback a fuentes del sistema
            self.fuentes = {
                'titulo': pygame.font.SysFont('Arial', 48, bold=True),
                'subtitulo': pygame.font.SysFont('Arial', 32),
                'boton': pygame.font.SysFont('Arial', 28, bold=True),
                'texto': pygame.font.SysFont('Arial', 24),
                'pequeño': pygame.font.SysFont('Arial', 20)
            }
    
    def obtener_fuente(self, tipo: str) -> pygame.font.Font:
        """Obtiene una fuente por tipo"""
        return self.fuentes.get(tipo, self.fuentes['texto'])
    
    def obtener_tema_actual(self) -> Dict[str, Any]:
        """Obtiene el tema visual actual"""
        return Tema.COLORES
    
    
    def registrar_ventana(self, tipo: TipoVentana, ventana: VentanaBase):
        """Registra una nueva ventana"""
        self.ventanas[tipo] = ventana
    
    def cambiar_ventana(self, tipo: TipoVentana, agregar_a_pila: bool = True):
        """Cambia a una ventana específica"""
        if tipo in self.ventanas:
            # Desactivar ventana actual
            if self.ventana_actual and self.ventana_actual in self.ventanas:
                self.ventanas[self.ventana_actual].desactivar()
                
                # Agregar a la pila para navegación hacia atrás
                if agregar_a_pila and self.ventana_actual != tipo:
                    self.pila_ventanas.append(self.ventana_actual)
            
            # Activar nueva ventana
            self.ventana_actual = tipo
            self.ventanas[tipo].activar()
    
    def volver_atras(self):
        """Vuelve a la ventana anterior"""
        if self.pila_ventanas:
            ventana_anterior = self.pila_ventanas.pop()
            self.cambiar_ventana(ventana_anterior, agregar_a_pila=False)
    
    def manejar_evento(self, evento: pygame.event.Event):
        """Maneja eventos de pygame"""
        if self.ventana_actual and self.ventana_actual in self.ventanas:
            self.ventanas[self.ventana_actual].manejar_evento(evento)
    
    def actualizar(self, dt: float):
        """Actualiza la ventana actual"""
        if self.ventana_actual and self.ventana_actual in self.ventanas:
            self.ventanas[self.ventana_actual].actualizar(dt)
    
    def renderizar(self, pantalla: pygame.Surface):
        """Renderiza la ventana actual"""
        if self.ventana_actual and self.ventana_actual in self.ventanas:
            tema = self.obtener_tema_actual()
            pantalla.fill(tema['fondo_principal'])
            self.ventanas[self.ventana_actual].renderizar(pantalla)
    
    def renderizar_boton(self, pantalla: pygame.Surface, boton: Dict):
        """Renderiza un botón estándar"""
        tema = self.obtener_tema_actual()
        
        # Determinar color
        color = boton['color_hover'] if boton.get('hover', False) else boton['color_normal']
        
        # Dibujar botón
        pygame.draw.rect(pantalla, color, boton['rect'], border_radius=8)
        pygame.draw.rect(pantalla, tema['texto_principal'], boton['rect'], 2, border_radius=8)
        
        # Dibujar texto
        fuente = self.obtener_fuente('boton')
        texto_surface = fuente.render(boton['texto'], True, tema['texto_principal'])
        texto_rect = texto_surface.get_rect(center=boton['rect'].center)
        pantalla.blit(texto_surface, texto_rect)
    
    def obtener_estadisticas(self):
        """Obtiene el gestor de estadísticas"""
        return self.gestor_datos
    
    def obtener_configuracion(self):
        """Obtiene el gestor de configuración"""
        return self.gestor_config