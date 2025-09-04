# 🎮 Tres en Raya con IA Minimax

Un juego de Tres en Raya implementado en Python con Pygame, que incluye una IA invencible basada en el algoritmo Minimax.

## 📂 Estructura del Proyecto

```
TresEnRaya/
├── main.py                      # 🚀 Punto de entrada principal del juego
├── requirements.txt             # 📦 Dependencias del proyecto
├── datos_juego.json             # 💾 Datos del juego (estadísticas + configuración)
├── logica/                      # 🧠 Lógica del juego y algoritmos
│   ├── logica_tablero.py       # 🎯 Reglas del tablero y validaciones
│   └── inteligencia_artificial.py # 🤖 IA con algoritmo Minimax
└── presentacion/               # 🎨 Interfaz gráfica y visualización
    ├── motor_principal.py      # 🔧 Motor principal del juego
    ├── sistema_navegacion.py   # 🧭 Sistema de navegación entre ventanas
    ├── menu_principal.py       # 📱 Menú principal y estadísticas
    ├── juego_clasico.py        # 🎮 Ventana del juego clásico
    ├── ventanas_auxiliares.py  # 🔧 Tutorial, historial y pausa
    └── efectos_multimedia.py   # ✨ Efectos visuales y animaciones
```

## 📄 Función de cada Archivo

### 🎯 Archivos Principales
- **`main.py`**: 
  - Punto de entrada minimalista del juego
  - Verifica dependencias básicas
  - Inicia el motor principal
  - Solo 25 líneas de código limpio

### 🧠 Carpeta `logica/`

#### **`logica_tablero.py`** - Lógica del Tablero
- **Responsabilidad**: Maneja todas las reglas del juego
- **Funciones principales**:
  - Matriz 3x3 del tablero
  - Validación de movimientos
  - Detección de condiciones de victoria
  - Control de turnos entre jugador e IA
  - Verificación de empates

#### **`inteligencia_artificial.py`** - IA Minimax
- **Responsabilidad**: Implementa la inteligencia artificial
- **Funciones principales**:
  - Algoritmo Minimax con poda alfa-beta
  - Evaluación heurística de posiciones
  - Cálculo del mejor movimiento para la IA
  - Estrategia optimizada (centro → esquinas → laterales)
  - Garantiza que la IA sea invencible

### 🎨 Carpeta `presentacion/`

#### **`motor_principal.py`** - Motor del Juego
- **Responsabilidad**: Coordina todo el sistema
- **Funciones principales**:
  - Inicialización de pygame
  - Bucle principal del juego
  - Gestión de eventos del usuario
  - Control de FPS y rendimiento
  - Configuración de ventana y audio

#### **`sistema_navegacion.py`** - Navegación
- **Responsabilidad**: Sistema de ventanas y navegación
- **Funciones principales**:
  - Gestión de múltiples ventanas
  - Sistema de navegación hacia atrás
  - Tema visual del juego (colores y fuentes)
  - Gestión de configuraciones
  - Sistema de estadísticas del jugador

#### **`menu_principal.py`** - Menú y Estadísticas
- **Responsabilidad**: Pantallas principales de información
- **Funciones principales**:
  - Menú principal con animaciones
  - Ventana de estadísticas detalladas
  - Partículas de fondo decorativas
  - Interfaz de navegación principal

#### **`juego_clasico.py`** - Juego Principal
- **Responsabilidad**: La experiencia de juego principal
- **Funciones principales**:
  - Renderizado del tablero visual
  - Manejo de clics e interacciones del usuario
  - Dibujado de símbolos X y O
  - Lógica de turnos y estados
  - Efectos visuales de victoria
  - Panel de controles lateral

#### **`ventanas_auxiliares.py`** - Ventanas Auxiliares
- **Responsabilidad**: Funcionalidades complementarias
- **Funciones principales**:
  - Tutorial interactivo paso a paso
  - Historial detallado de partidas
  - Ventana de pausa con opciones
  - Navegación auxiliar

#### **`efectos_multimedia.py`** - Efectos Visuales
- **Responsabilidad**: Efectos visuales y animaciones
- **Funciones principales**:
  - Animaciones de aparición de símbolos
  - Efectos de escala y transición
  - Sistema simplificado de partículas
  - Gestión de efectos temporales

## 🎮 Cómo Funciona Internamente

### 1. **Inicialización del Sistema**
```
main.py → motor_principal.py → sistema_navegacion.py
```
1. Verifica dependencias (pygame)
2. Inicializa el motor gráfico
3. Carga configuraciones y estadísticas
4. Registra todas las ventanas del sistema
5. Muestra el menú principal

### 2. **Flujo del Juego**
```
Menu Principal → Juego Clásico → Lógica del Tablero ↔ IA
```
1. **Usuario hace click en "JUGAR"**:
   - `menu_principal.py` → `juego_clasico.py`
   
2. **Inicialización del juego**:
   - `juego_clasico.py` crea instancias de `logica_tablero.py` e `inteligencia_artificial.py`
   
3. **Turno del jugador**:
   - Click del usuario → `juego_clasico.py` procesa coordenadas
   - `logica_tablero.py` valida y ejecuta el movimiento
   - `efectos_multimedia.py` anima la colocación del símbolo
   
4. **Turno de la IA**:
   - `inteligencia_artificial.py` calcula mejor movimiento usando Minimax
   - `logica_tablero.py` ejecuta el movimiento de la IA
   - Se verifica el estado del juego (victoria/empate/continúa)

### 3. **Algoritmo Minimax en Detalle**
El archivo `inteligencia_artificial.py` implementa:

- **Evaluación recursiva**: Explora todos los movimientos posibles
- **Maximización**: La IA busca maximizar su puntuación
- **Minimización**: Asume que el jugador humano minimizará la puntuación de la IA
- **Poda alfa-beta**: Elimina ramas innecesarias para optimizar el cálculo
- **Heurística**: Prefiere centro (5 pts) → esquinas (3 pts) → laterales (2 pts)

### 4. **Sistema de Navegación**
El archivo `sistema_navegacion.py` maneja:

- **Pila de ventanas**: Para navegación hacia atrás
- **Estados globales**: Configuraciones y estadísticas
- **Tema único**: Colores y fuentes consistentes
- **Gestión de eventos**: Distribución a la ventana activa

## 🚀 Instalación y Ejecución

1. **Instalar dependencias**:
   ```bash
   pip install pygame
   ```

2. **Ejecutar el juego**:
   ```bash
   python main.py
   ```

## 🎯 Controles del Juego

- **Ratón**: Hacer click en casillas para jugar
- **ESC**: Pausar el juego
- **R**: Reiniciar partida
- **M**: Volver al menú principal
- **F11**: Pantalla completa
- **F3**: Mostrar/ocultar FPS

## 💾 Archivos de Datos

- **`datos_juego.json`**: Estadísticas del jugador y configuración básica

## 🧑‍💻 Para Desarrolladores Principiantes

### Patrón de Arquitectura: **Separación por Responsabilidades**

El código está claramente dividido por funcionalidades:

1. **`logica/`** = **Modelo**: Las reglas puras del juego, sin interfaz
   - No depende de pygame ni gráficos
   - Se puede probar independientemente
   - Contiene la lógica de negocio

2. **`presentacion/`** = **Vista + Controlador**: Lo que ve y controla el usuario
   - Maneja pygame y gráficos
   - Procesa eventos del usuario
   - Coordina la lógica con la visualización

3. **Principio de Responsabilidad Única**: 
   - Cada archivo tiene **una sola razón para cambiar**
   - `logica_tablero.py` solo cambia si cambian las reglas
   - `efectos_multimedia.py` solo cambia si cambian los efectos
   - `inteligencia_artificial.py` solo cambia si mejora la IA

### Ventajas de esta Estructura:
- ✅ **Fácil mantenimiento**: Cada archivo tiene un propósito claro
- ✅ **Fácil testing**: Puedes probar la lógica sin la interfaz
- ✅ **Fácil extensión**: Agregar nuevos efectos o modos es sencillo
- ✅ **Fácil comprensión**: Los nombres de archivos indican su contenido
