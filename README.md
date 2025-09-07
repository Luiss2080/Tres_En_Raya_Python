# 🎮 Tres en Raya con IA Minimax

Un juego de Tres en Raya profesional implementado en Python con Pygame, que incluye una IA invencible basada en el algoritmo Minimax con poda alfa-beta. El proyecto está diseñado con arquitectura modular y principios de código limpio.

## ✨ Características Principales

- 🤖 **IA Invencible**: Algoritmo Minimax con poda alfa-beta
- 🎨 **Interfaz Moderna**: Gráficos fluidos con Pygame
- � **Sistema de Estadísticas**: Tracking completo de partidas y rendimiento
- 🎯 **Tutorial Interactivo**: Aprende a jugar paso a paso
- ⚡ **Efectos Visuales**: Animaciones suaves y efectos de partículas
- 📱 **Navegación Intuitiva**: Sistema de ventanas con navegación hacia atrás
- 💾 **Persistencia de Datos**: Guarda automáticamente estadísticas y configuración
- 🎮 **Controles Completos**: Soporte para teclado y ratón

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Luiss2080/Tres_En_Raya.git
   cd Tres_En_Raya
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el juego**:
   ```bash
   python main.py
   ```

## 📦 Dependencias

- `pygame==2.5.2` - Motor gráfico y de eventos
- `numpy==1.24.3` - Cálculos matemáticos optimizados

## �📂 Estructura del Proyecto

```
Tres_En_Raya/
├── main.py                      # 🚀 Punto de entrada principal
├── requirements.txt             # 📦 Dependencias del proyecto
├── configuracion_juego.json     # ⚙️ Configuración del juego
├── datos_juego.json             # 💾 Estadísticas y datos persistentes
├── logica/                      # 🧠 Lógica de negocio
│   ├── logica_tablero.py       # 🎯 Reglas del tablero y validaciones
│   └── inteligencia_artificial.py # 🤖 IA con algoritmo Minimax
└── presentacion/               # 🎨 Interfaz gráfica
    ├── motor_principal.py      # 🔧 Motor principal del juego
    ├── sistema_navegacion.py   # 🧭 Sistema de navegación
    ├── menu_principal.py       # 📱 Menú principal y estadísticas
    ├── juego_clasico.py        # 🎮 Pantalla de juego principal
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

## � Cómo Jugar

### Controles Básicos
- **Ratón**: Haz clic en cualquier casilla vacía para colocar tu símbolo (X)
- **ESC**: Pausar el juego en cualquier momento
- **R**: Reiniciar la partida actual
- **M**: Volver al menú principal
- **F11**: Alternar pantalla completa
- **F3**: Mostrar/ocultar contador de FPS

### Reglas del Juego
1. El jugador siempre juega con **X** y comienza primero
2. La IA juega con **O** y responde automáticamente
3. Gana quien consiga **tres símbolos en línea** (horizontal, vertical o diagonal)
4. Si se llenan todas las casillas sin ganador, es **empate**

### Navegación del Menú
- **JUGAR**: Iniciar nueva partida contra la IA
- **TUTORIAL**: Aprende las reglas paso a paso
- **ESTADÍSTICAS**: Ver tu historial de partidas
- **SALIR**: Cerrar el juego

## 🤖 Sobre la Inteligencia Artificial

### Algoritmo Minimax
La IA utiliza el famoso algoritmo **Minimax con poda alfa-beta** que:

- 🔍 **Explora todos los movimientos posibles** hasta el final del juego
- 🎯 **Evalúa cada posición** usando una función heurística optimizada
- ⚡ **Optimiza el cálculo** eliminando ramas innecesarias (poda alfa-beta)
- 🏆 **Garantiza el mejor movimiento** matemáticamente posible

### Estrategia de la IA
1. **Prioridad Centro**: 5 puntos - Controla el máximo de líneas
2. **Prioridad Esquinas**: 3 puntos - Múltiples oportunidades de victoria
3. **Prioridad Laterales**: 2 puntos - Menos versatilidad pero necesarios

> **¿Se puede ganar?** Técnicamente no, pero puedes conseguir empates si juegas perfectamente.

## 📊 Sistema de Estadísticas

El juego trackea automáticamente:

- 🎮 **Partidas jugadas** - Total de juegos completados
- 🏆 **Victorias/Derrotas/Empates** - Resultados detallados
- ⏱️ **Tiempo de juego** - Duración total y mejor tiempo
- 🔥 **Rachas** - Secuencias de victorias consecutivas
- 📅 **Historial** - Registro completo de partidas con fechas
- 🎯 **Primeros movimientos** - Análisis de estrategias iniciales

## � Archivos de Configuración

### `configuracion_juego.json`
```json
{
  "fps_objetivo": 60,        // FPS target del juego
  "mostrar_fps": false,      // Mostrar contador FPS
  "auto_guardar": true,      // Guardar automáticamente
  "modo_actual": "clasico"   // Modo de juego actual
}
```

### `datos_juego.json`
Almacena todas las estadísticas del jugador y el historial de partidas. Se actualiza automáticamente después de cada juego.

## 🏗️ Arquitectura del Código

### Patrón de Diseño: **Separación de Responsabilidades**

El proyecto sigue principios de **código limpio** con clara separación entre:

#### 📁 `logica/` - Capa de Negocio
- **Sin dependencias gráficas** - Lógica pura del juego
- **Completamente testeable** - Se puede probar independientemente
- **Reutilizable** - Fácil de portar a otras interfaces

#### 📁 `presentacion/` - Capa de Presentación
- **Interfaz gráfica** - Todo lo relacionado con Pygame
- **Eventos del usuario** - Manejo de input y navegación
- **Efectos visuales** - Animaciones y multimedia

### Componentes Clave

#### 🧠 `logica/logica_tablero.py`
```python
class TresEnRaya:
    # Matriz 3x3 del tablero
    # Validación de movimientos
    # Detección de victoria/empate
    # Control de turnos
```

#### 🤖 `logica/inteligencia_artificial.py`
```python
class AlgoritmoMinimax:
    # Implementación del algoritmo Minimax
    # Poda alfa-beta para optimización
    # Función de evaluación heurística
    # Cálculo del mejor movimiento
```

#### 🎮 `presentacion/motor_principal.py`
```python
class MotorJuegoAvanzado:
    # Inicialización de Pygame
    # Bucle principal del juego
    # Gestión de eventos globales
    # Control de FPS y rendimiento
```

#### 🧭 `presentacion/sistema_navegacion.py`
```python
class SistemaNavegacion:
    # Gestión de múltiples ventanas
    # Navegación hacia atrás
    # Tema visual consistente
    # Estado global del juego
```

## 🚀 Para Desarrolladores

### Extender el Juego

1. **Nuevos Modos de Juego**:
   - Crea una nueva clase en `presentacion/`
   - Hereda de `VentanaBase`
   - Regístrala en `sistema_navegacion.py`

2. **Mejorar la IA**:
   - Modifica `logica/inteligencia_artificial.py`
   - Ajusta la función de evaluación
   - Implementa diferentes niveles de dificultad

3. **Nuevos Efectos Visuales**:
   - Edita `presentacion/efectos_multimedia.py`
   - Agrega nuevas animaciones
   - Crea sistemas de partículas más complejos

### Principios Aplicados

- ✅ **Principio de Responsabilidad Única** - Cada clase tiene un propósito
- ✅ **Separación de Concerns** - Lógica separada de presentación
- ✅ **Código Autodocumentado** - Nombres descriptivos y claros
- ✅ **Configuración Externa** - Parámetros en archivos JSON
- ✅ **Manejo de Errores** - Try/catch apropiados

## 🐛 Resolución de Problemas

### Error: "Pygame no está instalado"
```bash
pip install pygame==2.5.2
```

### Error: "No se puede encontrar el módulo numpy"
```bash
pip install numpy==1.24.3
```

### El juego no inicia
1. Verifica que tienes Python 3.8+
2. Asegúrate de estar en el directorio correcto
3. Ejecuta: `python --version` y `pip list`

### Rendimiento lento
- Reduce FPS en `configuracion_juego.json`
- Cierra otras aplicaciones pesadas
- Actualiza controladores gráficos

## 📝 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una branch para tu feature
3. Commit tus cambios
4. Push a la branch
5. Abre un Pull Request

## 📞 Contacto

- **Desarrollador**: Luis
- **GitHub**: [@Luiss2080](https://github.com/Luiss2080)
- **Proyecto**: [Tres_En_Raya](https://github.com/Luiss2080/Tres_En_Raya)

---

⭐ **¡Dale una estrella al proyecto si te gusta!** ⭐
