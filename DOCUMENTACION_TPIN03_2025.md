# Trabajo Práctico Integrador Nro 03
## Sistema de Análisis de Robos Automotores – DNRPA

### 1. Carátula
- Integrantes: (Completar nombres completos)  
- Legajos: (Completar)  
- Comisión: (Completar)  
- Día de cursada: (Completar)  
- Grupo / Entrega: `GR.03_?_TPIN03_2025`  

---
### 2. Descripción General del Problema
El proyecto implementa un sistema interactivo en Python que descarga, procesa y analiza datos de robos y recuperos de vehículos registrados por DNRPA para el año 2025. A partir de múltiples archivos CSV contenidos en un ZIP oficial, se combinan los datos, se limpian y se generan métricas y visualizaciones que permiten:
- Identificar distribución de robos por provincias.
- Conocer marcas más afectadas.
- Analizar antigüedad de los vehículos involucrados.
- Observar la evolución temporal mensual.
- Consultar estadísticas específicas por provincia.

El enfoque sigue principios de diseño de algoritmos, modularidad, reutilización y separación de responsabilidades.

---
### 3. Dataset y Origen de Datos
- Fuente: Portal de datos públicos (URL por defecto provista en el script).  
- Formato de entrada: Archivo ZIP con múltiples archivos `.csv` (uno por mes u otros criterios).  
- Cantidad de columnas: (Según dataset original; tras transformación se reducen a 10 relevantes).  
- Cantidad de filas: Más de 200 (verificado al cargar múltiples CSV concatenados).  
- Carpeta destino tras extracción: `./datasets/`.

Cada CSV se lee con `pandas.read_csv` y se acumula en una lista para luego concatenarse en un único DataFrame unificado.

---
### 4. Arquitectura y Organización del Código
El proyecto se divide en:
- Archivo principal: `GR.03_3A_TPIN03_2025.py` (flujo interactivo y ejecución general).
- Módulo de análisis (en versión estática integrada): Clase `AnalizadorDatos` (métodos estáticos de transformación y consulta).  
- Clase `DatasetDownloader`: Maneja descarga y extracción del archivo ZIP.  
- Clase `AnalizadorRobosVehiculos`: Orquesta el ciclo completo de análisis (carga, proceso, métricas, gráficos y consultas).

Estructura de clases:
1. `DatasetDownloader`
   - Atributos privados: URL, carpeta destino, nombre de archivo.
   - Métodos: `descargar()`, `extraer_dataset()`.
2. `AnalizadorDatos`
   - Métodos estáticos: `cargar_datasets_csv`, `limpiar_y_transformar`, `calcular_edad_vehiculo`, `obtener_top_marcas`, `obtener_estadisticas_provincia`, `filtrar_por_rango_anios`.
3. `AnalizadorRobosVehiculos`
   - Atributos privados: DataFrames original y procesado, lista de provincias.
   - Métodos: `cargar_datos`, `procesar_datos`, `estadisticas_generales`, `analisis_por_provincia`, `analisis_marcas`, `grafico_provincias`, `grafico_marcas`, `grafico_antiguedad`, `grafico_evolucion_temporal`, `consulta_interactiva_provincia`, `ejecutar_analisis_completo`.

---
### 5. Transformaciones Realizadas (Requerimiento de al menos 3)
Sobre el DataFrame original se aplican:
1. Renombrado de columnas: Se ajustan nombres técnicos a nombres más claros (`tramite_tipo` → `tipo_tramite`, etc.).
2. Filtrado condicional: Se eliminan filas sin provincia o tipo de trámite y se descartan vehículos con `anio <= 1980` (ruido histórico no relevante para análisis actual).
3. Creación de columnas derivadas: `mes` y `anio_tramite` extraídas de la fecha original (`fecha_tramite`), más `antiguedad` (cálculo de edad del vehículo respecto a 2025).
4. Conversión de tipo: `fecha_tramite` convertida a tipo datetime con manejo de errores.
5. Subselección de columnas: Se reduce a un subconjunto relevante (10 columnas).

---
### 6. Métricas y Análisis Estadístico
El sistema calcula y muestra:
- Conteo total de registros (`total_robos`).
- Media, mediana y desviación estándar de antigüedad de vehículos robados.
- Conteo por categoría de `tipo_tramite` con porcentaje relativo.
- Top N marcas más afectadas (por frecuencia).
- Estats por provincia (total casos, antigüedad promedio, marca principal) en consulta dinámica.

Se emplea `numpy` para cálculos vectorizados: `mean`, `median`, `std` sobre arrays de antigüedad.

---
### 7. Visualizaciones (Matplotlib)
Se generan cuatro gráficos:
1. Barras: Top 10 provincias con mayor cantidad de robos.
2. Pie: Distribución porcentual de robos por marca (Top 5).
3. Histograma: Distribución de antigüedad de vehículos robados (se resalta bin que contiene la media).
4. Línea (Evolución temporal): Línea mensual con relleno debajo para tendencia.

Cada gráfico incluye etiquetas, título, estilo mínimo y ajustes de layout para legibilidad.

---
### 8. Flujo de Ejecución (Menú Interactivo)
1. Limpieza de pantalla e introducción.
2. Solicitud de URL (o usado valor por defecto si se deja vacío).
3. Descarga y extracción del ZIP.
4. Instanciación de `AnalizadorRobosVehiculos`.
5. Menú principal con opciones:
   - Opción 1: Análisis completo (carga, proceso, métricas y gráficos secuenciales).
   - Opción 2: Consulta específica por provincia.
   - Opción 3: Salir.
6. Validación de opción sin usar `while True` infinito (ciclo controlado).
7. Retorno al menú tras cada flujo hasta finalizar.

---
### 9. Uso de Requerimientos Básicos (Checklist)
- Tipos de variables: `str` (URL, provincias), `int` (años), `float` (estadísticas), `bool` (control de ejecución), `list` (rutas, provincias), `dict` (mapeo de columnas y estadísticas), tuples implícitas (enumerate).  
- Estructuras de control: `for`, `while`, condicionales `if/elif/else`.  
- Subrutinas propias: Múltiples métodos y funciones (`limpiar_pantalla`, métodos de clases).  
- Modularidad: Separación conceptual por clases (descarga, transformación, análisis).  
- Entradas: `input()` para URL, opción de menú y provincia buscada.  
- Salidas: `print()` para estado, resultados y guías al usuario.  
- Validaciones: Verificación de archivo existente, opción de menú válida, existencia de provincia.  
- Algoritmos de flujo: Menú interactivo y bucles de consulta.  

---
### 10. Diseño y Buenas Prácticas
- Nombres descriptivos para clases y métodos.
- Encapsulamiento de atributos con prefijo `__` en clases principales.
- Reutilización: Métodos estáticos en `AnalizadorDatos` evitan duplicación.
- Separación de responsabilidades: Cada clase atiende una dimensión del problema.
- Manejo de errores básico: Excepciones en descarga y extracción (HTTP y ZIP).

Posibles mejoras:
- Manejo de errores más granular (por ejemplo, columnas faltantes, formatos inesperados).
- Logging estructurado en lugar de `print` para auditoría.
- Parámetros configurables (año actual dinámico, filtros adaptativos).

---
### 11. Opcionales Implementados / Potenciales para Mejor Nota
IMPLEMENTADOS:
- Uso de Clases y POO (tres clases con responsabilidades claras).
- Uso de Numpy para métricas estadísticas vectorizadas.
- Múltiples gráficos (4, incluyendo histograma y línea que no son barras ni torta).

PENDIENTES / PROPUESTOS:
- Web Scraping o API: Integrar indicadores externos (ej. índice de parque automotor por provincia) y unir por clave de provincia.
- Normalización numérica: Normalizar antigüedad o crear una métrica escalada (min-max) para futuras comparaciones.
- Algoritmo supervisado: Entrenar un modelo simple (ej. regresión lineal para estimar probabilidad de robo según antigüedad y provincia) si se cuenta con variables suficientes.

---
### 12. Consideraciones Técnicas del Dataset
Suposiciones adoptadas:
- Registros con año de vehículo menor o igual a 1980 se consideran obsoletos para este análisis.
- Fecha de trámite se asume válida cuando puede parsearse; las inválidas se convierten en `NaT` (se mantienen sólo si permiten mes/año).
- Antigüedad calculada respecto a año fijo 2025 (configurable).

Impacto de decisiones:
- Eliminación de ruido permite estadísticas más centradas en el parque automotor moderno.
- Inclusión de marcas y provincias habilita segmentaciones comerciales y operativas.

---
### 13. Ejecución del Programa
Requisitos previos (según `requirements.txt`):
- pandas
- numpy
- matplotlib
- requests

Instalación (Windows PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python GR.03_3A_TPIN03_2025.py
```
Flujo esperado:
1. Usuario ingresa o acepta URL por defecto.
2. Se descarga y extrae ZIP.
3. Selecciona opción 1 (análisis completo) o 2 (consulta por provincia).
4. Visualiza gráficos y métricas.
5. Decide continuar o salir.

---
### 14. Conclusiones
El sistema cumple con los requisitos mínimos y agrega valor mediante visualizaciones y un flujo interactivo claro. La arquitectura permite extender funcionalidades (web scraping, machine learning, enriquecimiento regional). Se observa buen potencial para evolucionar hacia dashboards más avanzados o integración con otras fuentes de datos.

La solución demuestra:
- Aplicación correcta de transformación y análisis de datos.
- Uso apropiado de POO para separar tareas.
- Generación de métricas y visualizaciones interpretables.

---
### 15. Próximos Pasos / Extensiones Sugeridas
- Integrar tasas de recuperación vs robo para análisis comparativo.
- Añadir exportación de resultados a CSV/Excel.
- Implementar caché de descarga para evitar múltiples requests.
- Añadir pruebas unitarias (pytest) para funciones críticas.
- Parametrizar año base dinámico (`datetime.now().year`).

---
### 16. Conversión del Documento a Formato .doc/.docx
Opciones:
1. Copiar este contenido en Word y guardar como `.docx`.
2. Usar `pandoc`:
   ```bash
   pandoc DOCUMENTACION_TPIN03_2025.md -o DOCUMENTACION_TPIN03_2025.docx
   ```
3. Verificar carátula y completar datos faltantes antes de exportar.

---
### 17. Declaración de Integridad
Declaro que el código y la documentación fueron desarrollados con comprensión de cada parte, sin plagio y alineados a los objetivos del trabajo práctico. Cualquier asistencia automatizada fue verificada y adaptada al contexto del problema.

---
### 18. Anexos
Posibles anexos futuros: Ejemplos de salidas (capturas de gráficos), descripción de columnas originales, tabla de conteos por provincia completa.

---
Fin del documento.
