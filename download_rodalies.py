import os
import requests
import zipfile
import io
import shutil

# URL del archivo ZIP de Rodalies
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"

# Ruta donde guardar los archivos
data_dir = "data"

# Eliminar archivos previos excepto .gitkeep
for filename in os.listdir(data_dir):
    if filename != '.gitkeep':
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# Descargar ZIP
response = requests.get(url)
if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(data_dir)
    print("Archivo descargado y extraído con éxito.")
else:
    print("Error al descargar el archivo:", response.status_code)

# Filtrar stop_times.txt por líneas que contengan al menos una 'R' en trip_id
stop_times_path = os.path.join(data_dir, "stop_times.txt")
filtered_path = os.path.join(data_dir, "stop_times_filtered.txt")

with open(stop_times_path, "r", encoding="utf-8") as original, open(filtered_path, "w", encoding="utf-8") as filtered:
    header = original.readline()
    filtered.write(header)
    for line in original:
        if 'R' in line.split(',')[0]:
            filtered.write(line)




