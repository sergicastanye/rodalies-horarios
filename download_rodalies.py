import os
import requests
import zipfile
import io
import shutil

# URL del archivo ZIP
url = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"
data_dir = "data"

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
        # Extraer solo los archivos necesarios
        for name in z.namelist():
            if name.endswith(".txt") and not name.endswith("stop_times.txt"):
                z.extract(name, data_dir)
        # Procesar stop_times.txt directamente desde el ZIP sin guardarlo entero
        with z.open("stop_times.txt") as stop_times_file, open(os.path.join(data_dir, "stop_times_filtered.txt"), "w", encoding="utf-8") as filtered:
            lines = stop_times_file.read().decode("utf-8").splitlines()
            header = lines[0]
            filtered.write(header + "\n")
            for line in lines[1:]:
                if 'R' in line.split(',')[0]:
                    filtered.write(line + "\n")
    print("Archivos procesados y filtrados con éxito.")
else:
    print("Error al descargar el archivo:", response.status_code)




