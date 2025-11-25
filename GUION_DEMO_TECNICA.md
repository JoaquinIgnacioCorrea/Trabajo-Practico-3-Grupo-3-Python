# Guion Demo Técnica (≤ 3 minutos)
Proyecto: Sistema de Análisis de Robos Automotores – DNRPA
Archivo principal: `GR.03_3A_TPIN03_2025.py`

## Objetivo del Video
Mostrar la funcionalidad clave del sistema: descarga, procesamiento, métricas, visualizaciones y consultas, destacando buenas prácticas y extensibilidad.

---
## Cronograma por Sección
| Tiempo (aprox) | Sección |
| --------------- | ------- |
| 0:00 - 0:25 | Apertura y contexto |
| 0:25 - 0:55 | Setup y descarga dataset |
| 0:55 - 1:25 | Transformaciones y métricas |
| 1:25 - 2:15 | Visualizaciones (4 gráficos) |
| 2:15 - 2:40 | Consulta por provincia |
| 2:40 - 2:55 | Arquitectura y extensiones |
| 2:55 - 3:00 | Cierre |

---
## Guion Detallado
### 1. Apertura (0:00 - 0:25)
"Hola, soy [Nombre]. Presento el Sistema de Análisis de Robos Automotores de DNRPA 2025. El objetivo es integrar descarga de datos, limpieza, análisis estadístico y visualizaciones interactivas para entender patrones de robos y recuperos en Argentina."

### 2. Setup y Descarga (0:25 - 0:55)
Mostrar carpeta del proyecto y ejecutar:
```powershell
python GR.03_3A_TPIN03_2025.py
```
Texto sugerido:
"Al iniciar, el programa solicita la URL del dataset; si la dejo vacía usa una URL oficial por defecto. Descarga un ZIP, lo extrae y prepara múltiples archivos CSV que luego serán combinados en un único DataFrame."

### 3. Transformaciones y Métricas (0:55 - 1:25)
"El sistema aplica renombrado de columnas, filtrado (eliminando años <= 1980 y registros incompletos), genera columnas derivadas de fecha (mes y año) y calcula la antigüedad del vehículo respecto a 2025. Luego computa métricas estadísticas: total de casos, media, mediana y desviación estándar de antigüedad, además de la distribución por tipo de trámite. Todo esto se hace con Pandas y Numpy de forma vectorizada."

(Se puede hacer scroll rápido por el código: métodos en `AnalizadorDatos` y `AnalizadorRobosVehiculos`).

### 4. Visualizaciones (1:25 - 2:15)
"Al elegir la opción de análisis completo se generan cuatro gráficos:"
- "Barras: Top 10 provincias con mayor cantidad de robos."
- "Torta: Distribución de robos por marca (Top 5)."
- "Histograma: Distribución de antigüedad de los vehículos, resaltando la media."
- "Línea: Evolución mensual de robos durante el año."
"Estos gráficos permiten detectar concentración geográfica, marcas más afectadas y variación temporal."

### 5. Consulta por Provincia (2:15 - 2:40)
Seleccionar opción 2:
"La consulta interactiva permite ingresar una provincia y obtener total de robos, antigüedad promedio y marca predominante. Esto facilita análisis focalizado regional."

### 6. Arquitectura y Extensibilidad (2:40 - 2:55)
Mostrar estructura de clases:
"La organización se basa en tres clases: `DatasetDownloader` (descarga y extracción), `AnalizadorDatos` (métodos estáticos reutilizables de transformación), y `AnalizadorRobosVehiculos` (orquestación completa: métricas, gráficos y consultas). Esta separación facilita agregar futuras funciones como web scraping, normalización avanzada, o incluso un modelo supervisado."

### 7. Cierre (2:55 - 3:00)
"En síntesis: el sistema integra adquisición, limpieza, análisis y visualización en un flujo claro y extensible. Listo para evolucionar con más fuentes de datos y técnicas analíticas. Gracias."

---
## Puntos Clave a Resaltar Verbalmente
- Dataset real y múltiples CSV consolidados.
- Uso de POO y métodos estáticos para claridad y reutilización.
- Métricas estadísticas con Numpy.
- Cuatro tipos de gráficos (variedad + requerimientos opcionales).
- Menú interactivo sin bucles infinitos.
- Filtro de calidad de datos (año > 1980).

---
## Posibles Recortes si Falta Tiempo
- Reducir explicación del histograma y línea a una sola frase.
- Mencionar extensiones sin enumerarlas ("es extensible a web scraping y machine learning").

---
## Versión Ultra Breve (≤ 60 seg)
"Proyecto de análisis de robos automotores DNRPA 2025. Descarga y combina CSV de un ZIP oficial. Limpieza: renombrado, filtros y nuevas columnas de fecha y antigüedad. Métricas: total, media, mediana, desviación y distribución por trámite. Visualizaciones: barras por provincias, torta por marcas, histograma de antigüedad y línea temporal. Consulta interactiva por provincia. Arquitectura modular con tres clases que facilitan extensiones futuras. Listo para evolucionar con más datos y algoritmos." 

---
## Checklist Pre-Grabación
- Activar entorno virtual.
- Verificar instalación de dependencias.
- Limpiar carpeta `datasets/` para mostrar descarga.
- Maximizar ventana para legibilidad de gráficos.
- Preparar una provincia con datos (ej: "BUENOS AIRES" si existe en dataset) para consulta rápida.

---
## Comandos de Ejecución
```powershell
.venv\Scripts\Activate.ps1
python GR.03_3A_TPIN03_2025.py
```

---
## Sugerencias Técnicas
- Si un gráfico tarda: mencionar brevemente que depende del tamaño del dataset.
- Usar voz clara y no leer literal; adaptar a estilo personal.

---
Fin del guion.
