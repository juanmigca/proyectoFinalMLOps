import json
import os

# Cargamos la configuracion
with open("gen_config.json", "r") as f:
    config = json.load(f)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config["output_data_dir"]))

# Asegura que el directorio de salida exista
os.makedirs(output_dir, exist_ok=True)

# V