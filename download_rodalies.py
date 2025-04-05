import os
import requests
import zipfile
import io
import shutil
from datetime import datetime

# URL del archivo ZIP
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"
data_dir = "data"

# Fecha de descarga
download_date = datetime.utcnow().date().isoformat()  # formato YYYY-MM-DD

# Limpiar archivos antiguos excepto .gitkeep
for filename in os.listdir(data_dir):
    if filename != '.gitkeep':
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# Descargar y extraer ZIP en memoria
response = requests.get(url)
if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Extraer y añadir columna a todos los archivos .txt menos stop_times
        for name in z.namelist():
            if name.endswith(".txt") and not name.endswith("stop_times.txt"):
                with z.open(name) as f:
                    lines = f.read().decode("utf-8").splitlines()
                    header = lines[0] + ",download_date"
                    rows = [line + f",{download_date}" for line in lines[1:]]
                    output_path = os.path.join(data_dir, os.path.basename(name))
                    with open(output_path, "w", encoding="utf-8") as out:
                        out.write(header + "\n")
                        out.write("\n".join(rows))

        # Procesar stop_times.txt y crear stop_times_filtered.txt
        with z.open("stop_times.txt") as stop_times_file, open(os.path.join(data_dir, "stop_times_filtered.txt"), "w", encoding="utf-8") as filtered:
            lines = stop_times_file.read().decode("utf-8").splitlines()
            header = lines[0] + ",download_date"
            filtered.write(header + "\n")
            for line in lines[1:]:
                if 'R' in line.split(',')[0]:
                    filtered.write(line + f",{download_date}\n")

    print("Archivos procesados y filtrados con éxito.")
else:
    print("Error al descargar el archivo:", response.status_code)
