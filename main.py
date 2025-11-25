import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from funciones_analisis import (cargar_datasets_csv, limpiar_y_transformar, 
                                 calcular_edad_vehiculo, obtener_top_marcas,
                                 obtener_estadisticas_provincia, filtrar_por_rango_anios,
                                 validar_opcion_menu)
from dataset_downloader import DatasetDownloader


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


class AnalizadorRobosVehiculos:
    def __init__(self, carpeta_datos):
        self.__datos_originales = None
        self.__datos_procesados = None
        self.__carpeta = carpeta_datos
        self.__provincias_disponibles = []
    
    def cargar_datos(self):
        print("Cargando datos de robos de vehículos...")
        self.__datos_originales = cargar_datasets_csv(self.__carpeta)
        
        if self.__datos_originales is None:
            print("No se encontraron archivos CSV en la carpeta especificada")
            return False
        
        print(f"Total de registros cargados: {len(self.__datos_originales)}")
        return True
    
    def procesar_datos(self):
        print("\nProcesando y transformando datos...")
        self.__datos_procesados = limpiar_y_transformar(self.__datos_originales)
        self.__datos_procesados = calcular_edad_vehiculo(self.__datos_procesados)
        
        provincias_unicas = self.__datos_procesados['provincia'].dropna().unique()
        self.__provincias_disponibles = sorted(provincias_unicas)
        
        print(f"Registros después de limpieza: {len(self.__datos_procesados)}")
        print(f"Provincias con datos: {len(self.__provincias_disponibles)}")
    
    def estadisticas_generales(self):
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES DEL DATASET")
        print("="*60)
        
        total_robos = len(self.__datos_procesados)
        
        antiguedades = self.__datos_procesados['antiguedad'].values
        media_antiguedad = np.mean(antiguedades)
        mediana_antiguedad = np.median(antiguedades)
        desviacion_antiguedad = np.std(antiguedades)
        
        print(f"\nTotal de casos registrados: {total_robos}")
        print(f"Antigüedad promedio de vehículos robados: {media_antiguedad:.2f} años")
        print(f"Antigüedad mediana: {mediana_antiguedad:.0f} años")
        print(f"Desviación estándar de antigüedad: {desviacion_antiguedad:.2f} años")
        
        tipo_tramite_counts = self.__datos_procesados['tipo_tramite'].value_counts()
        print("\nDistribución por tipo de trámite:")
        for tramite, cantidad in tipo_tramite_counts.items():
            porcentaje = (cantidad / total_robos) * 100
            print(f"  {tramite}: {cantidad} ({porcentaje:.1f}%)")
        
        return {
            'total': total_robos,
            'media_antiguedad': media_antiguedad,
            'mediana_antiguedad': mediana_antiguedad
        }
    
    def analisis_por_provincia(self):
        print("\n" + "="*60)
        print("ANÁLISIS POR PROVINCIA")
        print("="*60)
        
        casos_por_provincia = self.__datos_procesados.groupby('provincia').size()
        casos_ordenados = casos_por_provincia.sort_values(ascending=False)
        
        print("\nTop 10 provincias con más casos:")
        for i, (provincia, cantidad) in enumerate(casos_ordenados.head(10).items(), 1):
            print(f"{i}. {provincia}: {cantidad} casos")
        
        return casos_ordenados
    
    def analisis_marcas(self):
        print("\n" + "="*60)
        print("ANÁLISIS DE MARCAS MÁS AFECTADAS")
        print("="*60)
        
        top_marcas = obtener_top_marcas(self.__datos_procesados, 5)
        
        print("\nTop 5 marcas más robadas:")
        for i, (marca, cantidad) in enumerate(top_marcas.items(), 1):
            print(f"{i}. {marca}: {cantidad} vehículos")
        
        return top_marcas
    
    def grafico_provincias(self, casos_por_provincia):
        top_10_provincias = casos_por_provincia.head(10)
        
        plt.figure(figsize=(12, 7))
        colores = plt.cm.viridis(np.linspace(0, 0.9, len(top_10_provincias)))
        barras = plt.bar(range(len(top_10_provincias)), top_10_provincias.values, color=colores)
        
        plt.xlabel('Provincia', fontsize=12)
        plt.ylabel('Cantidad de Robos', fontsize=12)
        plt.title('Top 10 Provincias con Mayor Cantidad de Robos de Vehículos', fontsize=14, pad=20)
        plt.xticks(range(len(top_10_provincias)), top_10_provincias.index, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def grafico_marcas(self, top_marcas):
        plt.figure(figsize=(10, 10))
        colores = plt.cm.Set3(np.linspace(0, 1, len(top_marcas)))
        
        plt.pie(top_marcas.values, labels=top_marcas.index, autopct='%1.1f%%', 
                colors=colores, startangle=90)
        plt.title('Distribución de Robos por Marca de Vehículo (Top 5)', fontsize=14, pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def grafico_antiguedad(self):
        antiguedades = self.__datos_procesados['antiguedad'].values
        
        plt.figure(figsize=(12, 7))
        
        conteo, bins, patches = plt.hist(antiguedades, bins=30, edgecolor='black', alpha=0.7)
        
        media = np.mean(antiguedades)
        
        for i, patch in enumerate(patches):
            if bins[i] <= media <= bins[i+1]:
                patch.set_facecolor('red')
            else:
                patch.set_facecolor('skyblue')
        
        plt.axvline(media, color='red', linestyle='--', linewidth=2, 
                   label=f'Media: {media:.1f} años')
        
        plt.xlabel('Antigüedad del Vehículo (años)', fontsize=12)
        plt.ylabel('Cantidad de Vehículos', fontsize=12)
        plt.title('Distribución de Antigüedad de Vehículos Robados', fontsize=14, pad=20)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def grafico_evolucion_temporal(self):
        casos_por_mes = self.__datos_procesados.groupby('mes').size()
        
        plt.figure(figsize=(12, 7))
        
        meses = casos_por_mes.index
        valores = casos_por_mes.values
        
        plt.plot(meses, valores, marker='o', linewidth=2, markersize=8, color='darkblue')
        plt.fill_between(meses, valores, alpha=0.3, color='lightblue')
        
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Cantidad de Robos', fontsize=12)
        plt.title('Evolución Mensual de Casos de Robos de Vehículos', fontsize=14, pad=20)
        plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def consulta_interactiva_provincia(self):
        print("\n" + "="*60)
        print("CONSULTA POR PROVINCIA")
        print("="*60)
        
        print("\nProvincias disponibles:")
        for provincia in self.__provincias_disponibles:
            print(f"  {provincia}")
        
        provincia_encontrada = False
        
        while not provincia_encontrada:
            provincia_buscar = input("\nIngrese el nombre de la provincia a consultar: ")
            
            stats = obtener_estadisticas_provincia(self.__datos_procesados, provincia_buscar)
            
            if stats is None:
                print(f"\nNo se encontraron datos para la provincia '{provincia_buscar}'")
                print("Por favor, verifique el nombre e intente nuevamente.")
            else:
                print(f"\nEstadísticas para {provincia_buscar}:")
                print(f"  Total de casos: {stats['total']}")
                print(f"  Antigüedad promedio: {stats['antiguedad_promedio']:.2f} años")
                print(f"  Marca más afectada: {stats['marca_principal']}")
                provincia_encontrada = True
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
    
    def ejecutar_analisis_completo(self):
        if not self.cargar_datos():
            return
        
        self.procesar_datos()
        
        stats_generales = self.estadisticas_generales()
        casos_provincia = self.analisis_por_provincia()
        top_marcas = self.analisis_marcas()
        
        print("\n" + "="*60)
        print("GENERANDO VISUALIZACIONES")
        print("="*60)
        
        self.grafico_provincias(casos_provincia)
        self.grafico_marcas(top_marcas)
        self.grafico_antiguedad()
        self.grafico_evolucion_temporal()
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()


def mostrar_menu():
    print("\n" + "="*60)
    print("SISTEMA DE ANÁLISIS DE ROBOS AUTOMOTORES - DNRPA")
    print("="*60)
    print("\n1. Análisis completo con visualizaciones")
    print("2. Consulta por provincia específica")
    print("3. Salir")
    print("\n" + "="*60)


if __name__ == "__main__":
    limpiar_pantalla()
    print("="*60)
    print("SISTEMA DE ANÁLISIS DE ROBOS AUTOMOTORES - DNRPA")
    print("="*60)
    print("\nPrimero necesitamos descargar el dataset")
    print("Ingrese la URL del archivo ZIP con los datos de DNRPA")
    print("(Ejemplo: https://datos.jus.gob.ar/dataset/.../download/...)")
    
    url_dataset = input("\nURL del dataset: ").strip()
    
    if not url_dataset:
        url_dataset = "https://datos.jus.gob.ar/dataset/a9bdfec2-0af4-433a-b810-38c91275a251/resource/c5eb0b07-c6e6-49f1-8ea0-165c957f5f94/download/dnrpa-robos-recuperos-autos-2025.zip"
        print(f"\nUsando URL por defecto...")
    
    carpeta_datasets = "./datasets"
    
    print("\nDescargando dataset...")
    downloader = DatasetDownloader(url_dataset, carpeta_datasets)
    downloader.descargar()
    downloader.extraer_dataset()
    
    print("\nDataset listo. Iniciando sistema de análisis...")
    input("Presione Enter para continuar...")
    limpiar_pantalla()
    
    analizador = AnalizadorRobosVehiculos(carpeta_datasets)
    
    ejecutando = True
    
    while ejecutando:
        mostrar_menu()
        opcion = validar_opcion_menu(['1', '2', '3'])
        
        if opcion == '1':
            limpiar_pantalla()
            analizador.ejecutar_analisis_completo()
        
        elif opcion == '2':
            limpiar_pantalla()
            if analizador._AnalizadorRobosVehiculos__datos_procesados is None:
                print("\nCargando datos necesarios...")
                analizador.cargar_datos()
                analizador.procesar_datos()
            analizador.consulta_interactiva_provincia()
        
        elif opcion == '3':
            limpiar_pantalla()
            print("\nFinalizando análisis. Hasta pronto.")
            ejecutando = False