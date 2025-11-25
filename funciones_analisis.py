import os
import pandas as pd
import numpy as np


def cargar_datasets_csv(carpeta):
    archivos = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.csv'):
            ruta_completa = os.path.join(carpeta, archivo)
            archivos.append(ruta_completa)
    
    dataframes = []
    for ruta in archivos:
        df = pd.read_csv(ruta)
        dataframes.append(df)
    
    if len(dataframes) > 0:
        datos_combinados = pd.concat(dataframes, ignore_index=True)
        return datos_combinados
    return None


def limpiar_y_transformar(df):
    columnas_renombradas = {
        'tramite_tipo': 'tipo_tramite',
        'tramite_fecha': 'fecha_tramite',
        'registro_seccional_provincia': 'provincia',
        'automotor_anio_modelo': 'anio',
        'automotor_tipo_descripcion': 'tipo_vehiculo',
        'automotor_marca_descripcion': 'marca',
        'automotor_uso_descripcion': 'uso',
        'titular_genero': 'genero_titular',
        'titular_anio_nacimiento': 'anio_nacimiento_titular',
        'titular_domicilio_provincia': 'provincia_titular'
    }
    
    df_transformado = df.rename(columns=columnas_renombradas)
    
    columnas_mantener = ['tipo_tramite', 'fecha_tramite', 'provincia', 'anio', 
                         'tipo_vehiculo', 'marca', 'uso', 'genero_titular', 
                         'anio_nacimiento_titular', 'provincia_titular']
    df_transformado = df_transformado[columnas_mantener]
    
    df_transformado = df_transformado[df_transformado['tipo_tramite'].notna()]
    df_transformado = df_transformado[df_transformado['provincia'].notna()]
    df_transformado = df_transformado[df_transformado['anio'] > 1980]
    
    df_transformado['fecha_tramite'] = pd.to_datetime(df_transformado['fecha_tramite'], errors='coerce')
    df_transformado['mes'] = df_transformado['fecha_tramite'].dt.month
    df_transformado['anio_tramite'] = df_transformado['fecha_tramite'].dt.year
    
    return df_transformado


def calcular_edad_vehiculo(df):
    anio_actual = 2025
    df['antiguedad'] = anio_actual - df['anio']
    return df


def obtener_top_marcas(df, cantidad=10):
    conteo_marcas = df['marca'].value_counts()
    return conteo_marcas.head(cantidad)


def obtener_estadisticas_provincia(df, provincia):
    df_provincia = df[df['provincia'] == provincia]
    
    if len(df_provincia) == 0:
        return None
    
    total_casos = len(df_provincia)
    promedio_antiguedad = df_provincia['antiguedad'].mean()
    marca_mas_robada = df_provincia['marca'].mode()[0] if len(df_provincia['marca'].mode()) > 0 else 'Sin datos'
    
    estadisticas = {
        'total': total_casos,
        'antiguedad_promedio': promedio_antiguedad,
        'marca_principal': marca_mas_robada
    }
    
    return estadisticas


def filtrar_por_rango_anios(df, anio_inicio, anio_fin):
    return df[(df['anio'] >= anio_inicio) & (df['anio'] <= anio_fin)]


def validar_opcion_menu(opciones_validas):
    while True:
        opcion = input("Ingrese su opción: ")
        if opcion in opciones_validas:
            return opcion
        print(f"Opción inválida. Ingrese una de las siguientes: {', '.join(opciones_validas)}")
