import os
import shutil
import requests
import zipfile
from datetime import datetime

# Crear carpeta para guardar los datos
today = datetime.today().strftime("%Y-%m-%d")
folder = f"data/{today}"
os.makedirs(folder, exist_ok=True)

# Descargar el archivo ZIP
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"
zip_path = f"{folder}/fomento_transit.zip"

with requests.get(url, stream=True) as r:
    with open(zip_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

# Descomprimir el archivo
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(folder)

# Borrar el ZIP
os.remove(zip_path)

print("✅ Datos de Rodalies descargados y extraídos correctamente.")
