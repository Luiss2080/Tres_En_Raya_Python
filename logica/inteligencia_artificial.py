import math
from .logica_tablero import TableroJuego

class AlgoritmoMinimax:
    def __init__(self, tablero_juego):
        self.tablero = tablero_juego
        self.simbolo_maximizador = tablero_juego.simbolo_jugador_ia  # 'O'
        self.simbolo_minimizador = tablero_juego.simbolo_jugador_humano  # 'X'
    
    #Evalua el estado del puntaje de alfa y beta
    def evaluar_estado_terminal(self, profundidad):
        """Evalúa el estado terminal del juego"""
        ganador = self.tablero.verificar_ganador()
        
        if ganador == self.simbolo_maximizador:  # IA gana
            return 10 - profundidad
        elif ganador == self.simbolo_minimizador:  # Humano gana
            return profundidad - 10
        else:  # Empate
            return 0
        
    #Establece los puntos +10 (IA) y -10 (Humano)
    def minimax(self, profundidad, es_turno_maximizador, alfa=-math.inf, beta=math.inf):
        """
        Algoritmo Minimax con poda alfa-beta
        """
        # Verificar estados terminales
        ganador = self.tablero.verificar_ganador()
        if ganador is not None or self.tablero.es_tablero_lleno():
            return self.evaluar_estado_terminal(profundidad)
        
        if es_turno_maximizador:
            # Turno de la IA (maximizador)
            valor_maximo = -math.inf
            
            for fila, columna in self.tablero.obtener_movimientos_disponibles():
                # Realizar movimiento
                self.tablero.realizar_movimiento(fila, columna, self.simbolo_maximizador)
                
                # Llamada recursiva
                valor_evaluacion = self.minimax(profundidad + 1, False, alfa, beta)
                
                # Deshacer movimiento
                self.tablero.deshacer_movimiento(fila, columna)
                
                # Actualizar valor máximo
                valor_maximo = max(valor_maximo, valor_evaluacion)
                
                # Poda alfa-beta
                alfa = max(alfa, valor_evaluacion)
                if beta <= alfa:
                    break  # Poda beta
            
            return valor_maximo
        
        else:
            # Turno del humano (minimizador)
            valor_minimo = math.inf
            
            for fila, columna in self.tablero.obtener_movimientos_disponibles():
                # Realizar movimiento
                self.tablero.realizar_movimiento(fila, columna, self.simbolo_minimizador)
                
                # Llamada recursiva
                valor_evaluacion = self.minimax(profundidad + 1, True, alfa, beta)
                
                # Deshacer movimiento
                self.tablero.deshacer_movimiento(fila, columna)
                
                # Actualizar valor mínimo
                valor_minimo = min(valor_minimo, valor_evaluacion)
                
                # Poda alfa-beta
                beta = min(beta, valor_evaluacion)
                if beta <= alfa:
                    break  # Poda alfa
            
            return valor_minimo
    
    #Analiza el estado del juego para determinar el mejor movimiento
    def obtener_mejor_movimiento_ia(self):
        """
        Encuentra el mejor movimiento para la IA usando Minimax
        
        Returns:
            Tupla (fila, columna) del mejor movimiento
        """
        mejor_puntuacion = -math.inf
        mejor_movimiento = None
        movimientos_disponibles = self.tablero.obtener_movimientos_disponibles()
        
        # Si no hay movimientos disponibles
        if not movimientos_disponibles:
            return None
        
        # Si solo queda un movimiento, tomarlo directamente
        if len(movimientos_disponibles) == 1:
            return movimientos_disponibles[0]
        
        # Evaluar todos los movimientos posibles
        for fila, columna in movimientos_disponibles:
            # Realizar movimiento temporal
            self.tablero.realizar_movimiento(fila, columna, self.simbolo_maximizador)
            
            # Evaluar el movimiento usando minimax
            puntuacion_movimiento = self.minimax(0, False)
            
            # Deshacer movimiento temporal
            self.tablero.deshacer_movimiento(fila, columna)
            
            # Actualizar mejor movimiento si es necesario
            if puntuacion_movimiento > mejor_puntuacion:
                mejor_puntuacion = puntuacion_movimiento
                mejor_movimiento = (fila, columna)
        
        return mejor_movimiento
    
    #Ordena los movimientos por prioridad estratégica
    def obtener_movimientos_ordenados(self):
        """
        Ordena los movimientos por prioridad estratégica
        Centro > Esquinas > Laterales
        """
        movimientos_disponibles = self.tablero.obtener_movimientos_disponibles()
        
        # Definir prioridades de posiciones
        prioridades = {
            (1, 1): 3,  # Centro - máxima prioridad
            (0, 0): 2, (0, 2): 2, (2, 0): 2, (2, 2): 2,  # Esquinas
            (0, 1): 1, (1, 0): 1, (1, 2): 1, (2, 1): 1   # Laterales
        }
        
        # Ordenar movimientos por prioridad (mayor prioridad primero)
        movimientos_ordenados = sorted(
            movimientos_disponibles,
            key=lambda pos: prioridades.get(pos, 0),
            reverse=True
        )
        
        return movimientos_ordenados
    
    #Analiza la posición actual del tablero
    def analizar_posicion_actual(self):
        """
        Analiza la posición actual del tablero
        
        Returns:
            Diccionario con información del análisis
        """
        ganador = self.tablero.verificar_ganador()
        movimientos_disponibles = len(self.tablero.obtener_movimientos_disponibles())
        
        estado = "En juego"
        if ganador == self.simbolo_maximizador:
            estado = "IA ganó"
        elif ganador == self.simbolo_minimizador:
            estado = "Humano ganó"
        elif self.tablero.es_empate():
            estado = "Empate"
        
        return {
            "estado": estado,
            "ganador": ganador,
            "movimientos_restantes": movimientos_disponibles,
            "tablero_lleno": self.tablero.es_tablero_lleno()
        }