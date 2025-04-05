import os
import requests
from zipfile import ZipFile
from io import BytesIO

# URL del ZIP
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"

# Carpeta de salida
folder = "data"
os.makedirs(folder, exist_ok=True)

# Descargar el ZIP
response = requests.get(url)
if response.status_code == 200:
    zipfile = ZipFile(BytesIO(response.content))
    zipfile.extractall(folder)
    print("Archivo descargado y extraído con éxito.")
else:
    print("Error al descargar el archivo.")


