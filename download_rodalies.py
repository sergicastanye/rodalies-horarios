import os
import requests
import zipfile
from io import BytesIO

# URL del ZIP de Renfe
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"

# Descarga y extracción
response = requests.get(url)
with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
    zip_file.extractall("data")

# Ruta del archivo original y filtrado
input_path = "data/stop_times.txt"
output_path = "data/stop_times_filtered.txt"

# Filtrar por trip_id que contenga "R"
with open(input_path, "r", encoding="utf-8") as f_in:
    header = f_in.readline()
    filtered_lines = [line for line in f_in if "R" in line.split(",")[0]]

with open(output_path, "w", encoding="utf-8") as f_out:
    f_out.write(header)
    f_out.writelines(filtered_lines)

# Eliminar el archivo completo para evitar errores de tamaño
os.remove(input_path)



