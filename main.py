#!/usr/bin/env python3
"""
Tres en Raya con IA Minimax
Punto de entrada principal del juego
"""

import sys
import os

# Agregar carpeta actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal del juego"""
    try:
        import pygame
    except ImportError:
        print("ERROR: Pygame no esta instalado.")
        print("SOLUCION: Instala con: pip install pygame")
        return 1
    
    try:
        from presentacion.motor_principal import MotorJuegoAvanzado
        
        # Crear y ejecutar el juego
        motor = MotorJuegoAvanzado()
        motor.ejecutar()
        
    except Exception as e:
        print(f"ERROR al iniciar el juego: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())