import pandas as pd
import numpy as np
import os
import requests
import zipfile
import os
from matplotlib import pyplot as plt


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

class DatasetDownloader:
    def __init__(self, url, save_dir):
        self.__url = url
        self.__save_dir = save_dir
        self.__filename = os.path.join(save_dir, os.path.basename(url))

    def descargar(self):
        if os.path.exists(self.__filename):
            print(f"El archivo '{self.__filename}' ya existe. No se descargará de nuevo.")
        else:
            try:
                response = requests.get(self.__url, stream=True)
                response.raise_for_status()
                os.makedirs(self.__save_dir, exist_ok=True)
                with open(self.__filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Archivo descargado exitosamente y guardado en '{self.__filename}'.")
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar el archivo: {e}")
    
    def extraer_dataset(self):
        if not os.path.exists(self.__filename):
            print(f"El archivo '{self.__filename}' no existe. No se puede extraer.")
        else:
            try:
                with zipfile.ZipFile(self.__filename, 'r') as zip_ref:
                    zip_ref.extractall(self.__save_dir)
                os.remove(self.__filename)
                print(f"Archivo extraído exitosamente en '{self.__save_dir}'.")
            except zipfile.BadZipFile as e:
                print(f"Error al extraer el archivo ZIP: {e}")

class AnalizadorDatos:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def calcular_edad_vehiculo(df):
        anio_actual = 2025
        df['antiguedad'] = anio_actual - df['anio']
        return df



    @staticmethod
    def obtener_top_marcas(df, cantidad=10):
        conteo_marcas = df['marca'].value_counts()
        return conteo_marcas.head(cantidad)

    @staticmethod
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

    @staticmethod
    def filtrar_por_rango_anios(df, anio_inicio, anio_fin):
        return df[(df['anio'] >= anio_inicio) & (df['anio'] <= anio_fin)]


class AnalizadorRobosVehiculos:
    def __init__(self, carpeta_datos):
        self.__datos_originales = None
        self.__datos_procesados = None
        self.__carpeta = carpeta_datos
        self.__provincias_disponibles = []
    
    def cargar_datos(self):
        print("Cargando datos de robos automotores...")
        self.__datos_originales = AnalizadorDatos.cargar_datasets_csv(self.__carpeta)
        
        if self.__datos_originales is None:
            print("No se encontraron archivos CSV en la carpeta especificada")
            return False
        
        print(f"Total de registros cargados: {len(self.__datos_originales)}")
        return True
    
    def procesar_datos(self):
        print("\nProcesando y transformando datos...")
        self.__datos_procesados = AnalizadorDatos.limpiar_y_transformar(self.__datos_originales)
        self.__datos_procesados = AnalizadorDatos.calcular_edad_vehiculo(self.__datos_procesados)
        
        provincias_unicas = self.__datos_procesados['provincia'].dropna().unique()
        self.__provincias_disponibles = sorted(provincias_unicas)
        
        print(f"Registros después de limpieza: {len(self.__datos_procesados)}")
        print(f"Provincias con datos: {len(self.__provincias_disponibles)}")
    
    def estadisticas_generales(self):
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES")
        print("="*60)
        
        total_robos = len(self.__datos_procesados)
        
        antiguedades = self.__datos_procesados['antiguedad'].values
        media_antiguedad = np.mean(antiguedades)
        mediana_antiguedad = np.median(antiguedades)
        desviacion_antiguedad = np.std(antiguedades)
        
        print(f"\nTotal de robos registrados: {total_robos}")
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
        
        print("\nTop 10 provincias con más robos:")
        for i, (provincia, cantidad) in enumerate(casos_ordenados.head(10).items(), 1):
            print(f"{i}. {provincia}: {cantidad} robos")
        
        return casos_ordenados
    
    def analisis_marcas(self):
        print("\n" + "="*60)
        print("ANÁLISIS DE MARCAS MÁS AFECTADAS")
        print("="*60)
        
        top_marcas = AnalizadorDatos.obtener_top_marcas(self.__datos_procesados, 5)
        
        print("\nTop 5 marcas más robadas:")
        for i, (marca, cantidad) in enumerate(top_marcas.items(), 1):
            print(f"{i}. {marca}: {cantidad} vehículos")
        
        return top_marcas
    
    def grafico_provincias(self, casos_por_provincia):
        top_10_provincias = casos_por_provincia.head(10)
        
        plt.figure(figsize=(12, 7))
        colores = plt.cm.viridis(np.linspace(0, 0.9, len(top_10_provincias)))
        plt.bar(range(len(top_10_provincias)), top_10_provincias.values, color=colores)
        plt.xlabel('Provincia', fontsize=12)
        plt.ylabel('Cantidad de Robos', fontsize=12)
        plt.title('Top 10 Provincias con Mayor Cantidad de Robos Automotores', fontsize=14, pad=20)
        plt.xticks(range(len(top_10_provincias)), top_10_provincias.index, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def grafico_marcas(self, top_marcas):
        plt.figure(figsize=(10, 10))
        colores = plt.cm.Set3(np.linspace(0, 1, len(top_marcas)))
        
        plt.pie(top_marcas.values, labels=top_marcas.index, autopct='%1.1f%%', 
                colors=colores, startangle=90)
        plt.title('Distribución de Robos por Marca del Vehículo (Top 5)', fontsize=14, pad=20)
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
        plt.title('Evolución Mensual de Robos Automotores', fontsize=14, pad=20)
        plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def consulta_interactiva_provincia(self):
        print("\n" + "="*60)
        print("CONSULTA POR PROVINCIA")
        print("="*60)
        
        print("\nProvincias con datos:")
        for provincia in self.__provincias_disponibles:
            print(f"  {provincia}")
        
        provincia_encontrada = False
        
        while not provincia_encontrada:
            provincia_buscar = input("\nIngrese el nombre de la provincia a consultar: ")
            
            stats = AnalizadorDatos.obtener_estadisticas_provincia(self.__datos_procesados, provincia_buscar)
            
            if stats is None:
                print(f"\nNo se encontraron datos para la provincia '{provincia_buscar}'")
                print("Por favor, verifique el nombre e intente nuevamente.")
            else:
                print(f"\nEstadísticas para {provincia_buscar}:")
                print(f"  Total de robos: {stats['total']}")
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
    print("2. Consulta por provincia")
    print("3. Salir")
    print("\n" + "="*60)



limpiar_pantalla()
print("="*60)
print("SISTEMA DE ANÁLISIS DE ROBOS AUTOMOTORES - DNRPA")
print("="*60)
print("\nPrimero necesitamos descargar el dataset")
print("Ingrese la URL del archivo ZIP con los datos de DNRPA")
print("(Ejemplo: https://datos.jus.gob.ar/dataset/.../download/...)")
print("O presione Enter para usar la URL por defecto.")

url_dataset = input("\nURL del dataset: ")

if not url_dataset:
    url_dataset = "https://datos.jus.gob.ar/dataset/a9bdfec2-0af4-433a-b810-38c91275a251/resource/c5eb0b07-c6e6-49f1-8ea0-165c957f5f94/download/dnrpa-robos-recuperos-autos-2025.zip"
    print("\nUsando URL por defecto...")

carpeta_datasets = "./datasets"

print("\nDescargando dataset...")
downloader = DatasetDownloader(url_dataset, carpeta_datasets)
downloader.descargar()
downloader.extraer_dataset()

print("\nDataset descargado.")
input("Presione Enter para continuar...")
limpiar_pantalla()

analizador = AnalizadorRobosVehiculos(carpeta_datasets)

ejecutando = True
while ejecutando:
    mostrar_menu()
    opcion = None
    while opcion is None:
        opcion = input("Ingrese su opción: ")
        if opcion not in ['1', '2', '3']:
            print(f"Opción inválida. Ingrese una de las siguientes: 1, 2, 3")
            opcion = None
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