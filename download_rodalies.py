import os
import shutil
import requests
import zipfile

# Ruta fija para los datos
folder = "data/latest"

# Borrar todo si existe
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder, exist_ok=True)

# Descargar el archivo ZIP
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"
zip_path = f"{folder}/fomento_transit.zip"

with requests.get(url, stream=True) as r:
    with open(zip_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

# Descomprimir el ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(folder)

# Borrar el ZIP
os.remove(zip_path)

print("✅ Datos actualizados en carpeta fija: /data/latest/")

