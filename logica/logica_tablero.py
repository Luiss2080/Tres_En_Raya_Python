class TableroJuego:
    def __init__(self):
        self.matriz_tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.simbolo_jugador_humano = 'X'
        self.simbolo_jugador_ia = 'O'
        self.jugador_actual = self.simbolo_jugador_humano
        
        # Vectores para definir las posiciones ganadoras
        self.vectores_filas = [
            [(0, 0), (0, 1), (0, 2)],  # Fila 0
            [(1, 0), (1, 1), (1, 2)],  # Fila 1
            [(2, 0), (2, 1), (2, 2)]   # Fila 2
        ]
        
        self.vectores_columnas = [
            [(0, 0), (1, 0), (2, 0)],  # Columna 0
            [(0, 1), (1, 1), (2, 1)],  # Columna 1
            [(0, 2), (1, 2), (2, 2)]   # Columna 2
        ]
        
        self.vectores_diagonales = [
            [(0, 0), (1, 1), (2, 2)],  # Diagonal principal
            [(0, 2), (1, 1), (2, 0)]   # Diagonal secundaria
        ]
        
        # Todas las combinaciones ganadoras
        self.todas_las_combinaciones_ganadoras = (
            self.vectores_filas + 
            self.vectores_columnas + 
            self.vectores_diagonales
        )
    
    def reiniciar_tablero(self):
        """Reinicia el tablero a su estado inicial"""
        self.matriz_tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.jugador_actual = self.simbolo_jugador_humano
    
    def obtener_estado_tablero(self):
        """Retorna una copia del estado actual del tablero"""
        return [fila[:] for fila in self.matriz_tablero]
    
    def es_posicion_valida(self, fila, columna):
        """Verifica si una posición es válida y está disponible"""
        return (0 <= fila < 3 and 
                0 <= columna < 3 and 
                self.matriz_tablero[fila][columna] == ' ')
    
    def realizar_movimiento(self, fila, columna, simbolo_jugador):
        """Realiza un movimiento en el tablero"""
        if self.es_posicion_valida(fila, columna):
            self.matriz_tablero[fila][columna] = simbolo_jugador
            return True
        return False
    
    def deshacer_movimiento(self, fila, columna):
        """Deshace un movimiento (usado por minimax)"""
        self.matriz_tablero[fila][columna] = ' '
    
    def verificar_ganador_por_vector(self, vector_posiciones):
        """Verifica si hay un ganador en un vector específico"""
        simbolos = []
        for fila, columna in vector_posiciones:
            simbolos.append(self.matriz_tablero[fila][columna])
        
        # Si todos los símbolos son iguales y no están vacíos
        if simbolos[0] != ' ' and simbolos[0] == simbolos[1] == simbolos[2]:
            return simbolos[0]
        return None
    
    def verificar_ganador(self):
        """Verifica si hay un ganador usando todos los vectores"""
        for combinacion in self.todas_las_combinaciones_ganadoras:
            ganador = self.verificar_ganador_por_vector(combinacion)
            if ganador:
                return ganador
        return None
    
    def es_tablero_lleno(self):
        """Verifica si el tablero está completamente lleno"""
        for fila in range(3):
            for columna in range(3):
                if self.matriz_tablero[fila][columna] == ' ':
                    return False
        return True
    
    def es_empate(self):
        """Verifica si el juego terminó en empate"""
        return self.es_tablero_lleno() and self.verificar_ganador() is None
    
    def obtener_movimientos_disponibles(self):
        """Retorna una lista de todas las posiciones disponibles"""
        movimientos_disponibles = []
        for fila in range(3):
            for columna in range(3):
                if self.matriz_tablero[fila][columna] == ' ':
                    movimientos_disponibles.append((fila, columna))
        return movimientos_disponibles
    
    def mostrar_tablero_consola(self):
        """Muestra el tablero en consola para debug"""
        print("\n   0   1   2")
        for i, fila in enumerate(self.matriz_tablero):
            print(f"{i}  {' | '.join(fila)}")
            if i < 2:
                print("   ---------")
        print()
    
    def obtener_coordenadas_posicion(self, posicion):
        """Convierte una posición (0-8) a coordenadas (fila, columna)"""
        return posicion // 3, posicion % 3
    
    def obtener_posicion_coordenadas(self, fila, columna):
        """Convierte coordenadas (fila, columna) a posición (0-8)"""
        return fila * 3 + columna