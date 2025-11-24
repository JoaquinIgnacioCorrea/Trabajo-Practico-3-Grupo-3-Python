import os
import requests
import zipfile
class DatasetDownloader:
    def __init__(self, url, save_dir):
        self.__url = url
        self.__save_dir = save_dir
        self.__filename = os.path.join(save_dir, os.path.basename(url))

    def descargar(self):
        if os.path.exists(self.__filename):
            print(f"El archivo '{self.__filename}' ya existe. No se descargará de nuevo.")
            return
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
                print(f"Archivo extraído exitosamente en '{self.__save_dir}'.")
            except zipfile.BadZipFile as e:
                print(f"Error al extraer el archivo ZIP: {e}")