# Análisis de Robos de Vehículos - DNRPA 2025

## Descripción del Proyecto

Este proyecto realiza un análisis exhaustivo de los datos de robos y recuperos de vehículos en Argentina durante el año 2025, utilizando información oficial de la Dirección Nacional de los Registros Nacionales de la Propiedad del Automotor (DNRPA).

## Problema Abordado

El incremento en los robos de vehículos representa un problema significativo en Argentina. Este sistema permite:
- Identificar patrones geográficos de robos
- Determinar las marcas y modelos más afectados
- Analizar la evolución temporal de los incidentes
- Calcular estadísticas clave para la toma de decisiones

## Características Principales

### Funcionalidades Implementadas

1. **Carga Automatizada de Datos**: Integra múltiples archivos CSV de forma automática
2. **Transformación de Datos**: Limpieza, renombrado y creación de nuevas columnas
3. **Análisis Estadístico**: Cálculo de promedios, medianas y desviaciones
4. **Visualizaciones Interactivas**: 4 tipos diferentes de gráficos usando Matplotlib
5. **Consultas Personalizadas**: Búsqueda de estadísticas por provincia
6. **Interfaz de Menú**: Sistema interactivo con validación de entradas

### Tecnologías Utilizadas

- **Python 3.11+**
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas y estadísticas
- **Matplotlib**: Generación de visualizaciones
- **Requests**: Descarga de datasets (web_scrapper.py)
- **BeautifulSoup4**: Web scraping (web_scrapper.py)

## Estructura del Proyecto

```
Trabajo-Practico-3-Grupo-3-Python/
│
├── main.py                    # Programa principal con clase AnalizadorRobosVehiculos
├── funciones_analisis.py      # Módulo de funciones auxiliares
├── dataset_downloader.py      # Descarga automática de datasets
├── web_scrapper.py           # Herramienta de scraping web
├── requirements.txt          # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
│
└── datasets/                # Carpeta con archivos CSV (10 archivos mensuales)
    ├── dnrpa-robos-recuperos-autos-202501.csv
    ├── dnrpa-robos-recuperos-autos-202502.csv
    └── ... (8 archivos más)
```

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/JoaquinIgnacioCorrea/Trabajo-Practico-3-Grupo-3-Python.git
cd Trabajo-Practico-3-Grupo-3-Python
```

### 2. Crear entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar el programa

```powershell
python main.py
```

## Uso del Sistema

Al ejecutar `main.py`, se presenta un menú con las siguientes opciones:

1. **Análisis completo con visualizaciones**: Ejecuta todo el proceso de análisis y genera 4 gráficos
2. **Consulta por provincia específica**: Permite buscar estadísticas de una provincia particular
3. **Estadísticas rápidas**: Muestra resumen estadístico sin generar gráficos
4. **Salir**: Finaliza el programa

### Ejemplo de Uso

```
SISTEMA DE ANÁLISIS DE ROBOS DE VEHÍCULOS - DNRPA 2025
============================================================

1. Análisis completo con visualizaciones
2. Consulta por provincia específica
3. Estadísticas rápidas
4. Salir

Ingrese su opción: 1
```

## Transformaciones Realizadas

1. **Renombrado de columnas**: Se renombran todas las columnas a nombres más descriptivos
2. **Filtrado condicional**: Se eliminan registros con datos faltantes y vehículos anteriores a 1980
3. **Creación de columnas nuevas**: 
   - `antiguedad`: Edad del vehículo
   - `mes`: Mes del trámite
   - `anio_tramite`: Año del trámite
4. **Conversión de tipos**: Transformación de fechas a formato datetime
5. **Eliminación de columnas**: Se mantienen solo las columnas relevantes para el análisis

## Métricas Estadísticas Calculadas

1. **Media de antigüedad**: Promedio de años de los vehículos robados
2. **Mediana de antigüedad**: Valor central de la distribución
3. **Desviación estándar**: Dispersión de la antigüedad
4. **Conteos por categoría**: Distribución de casos por provincia, marca y tipo de trámite
5. **Análisis temporal**: Evolución mensual de casos

## Visualizaciones Generadas

1. **Gráfico de Barras**: Top 10 provincias con más robos (con gradiente de colores)
2. **Gráfico de Torta**: Distribución porcentual por marca (Top 15)
3. **Histograma**: Distribución de antigüedad de vehículos robados
4. **Gráfico de Líneas**: Evolución temporal mensual de casos

## Implementación con POO

La clase `AnalizadorRobosVehiculos` encapsula toda la lógica del análisis:

- **Atributos privados**: `__datos_originales`, `__datos_procesados`, `__carpeta`, `__provincias_disponibles`
- **Métodos públicos**: 
  - `cargar_datos()`: Carga los CSV
  - `procesar_datos()`: Aplica transformaciones
  - `estadisticas_generales()`: Calcula métricas
  - `analisis_por_provincia()`: Agrupa por ubicación
  - `analisis_marcas()`: Identifica marcas más afectadas
  - `grafico_*()`: Métodos para cada visualización
  - `ejecutar_analisis_completo()`: Workflow completo

## Uso de NumPy

Se utiliza NumPy para operaciones vectorizadas:
- Cálculo de promedios: `np.mean()`
- Cálculo de medianas: `np.median()`
- Desviaciones estándar: `np.std()`
- Generación de rangos de colores: `np.linspace()`

## Requisitos del TPIN03 Cumplidos

### Para Nota 7 (Básicos)
- ✅ Dataset con más de 5 columnas y 200 filas (10 archivos CSV con ~4000 registros cada uno)
- ✅ Uso de Pandas para lectura y transformación
- ✅ Al menos 3 transformaciones aplicadas (5 implementadas)
- ✅ Cálculo de 2+ métricas estadísticas (5 implementadas)
- ✅ Generación de gráfico con Matplotlib (4 gráficos diferentes)
- ✅ Código en archivo .py
- ✅ Variables de distintos tipos (int, float, str, bool)
- ✅ Tuplas, listas y diccionarios
- ✅ Estructuras for y while
- ✅ 2+ funciones definidas (8 funciones en módulo auxiliar)
- ✅ Separación en módulos (main.py y funciones_analisis.py)
- ✅ Comentarios y nombres significativos
- ✅ Input/print para interacción
- ✅ Menús y validaciones

### Para Nota 8-10 (Opcionales)
- ✅ **Uso de Clases (POO)**: Clase `AnalizadorRobosVehiculos` con atributos privados y métodos
- ✅ **Uso de NumPy**: Operaciones vectorizadas para cálculos estadísticos
- ✅ **Múltiples gráficos**: 4 tipos diferentes (barras, torta, histograma, líneas)
- ✅ **Gráficos avanzados**: Histograma y gráfico de líneas (no son barras ni torta)

## Resultados Esperados

El análisis permite identificar:
- Provincias con mayor incidencia de robos
- Marcas de vehículos más vulnerables
- Edad promedio de los vehículos robados
- Tendencias temporales en los robos

## Autor

Proyecto desarrollado para el Trabajo Práctico Integrador N°03 de la materia Python.

## Licencia

Este proyecto es de uso académico.
