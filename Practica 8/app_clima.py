from flask import Flask, jsonify
from flask_cors import CORS
import json  # 1. Importamos el módulo json

app = Flask(__name__)
CORS(app)

# --- Base de datos desde JSON ---
# 2. Creamos una función para cargar los datos del clima
def cargar_db_clima():
    """
    Lee el archivo JSON del clima y lo carga en memoria.
    """
    with open('clima.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 3. Cargamos los datos UNA VEZ cuando el servidor se inicia
db_clima = cargar_db_clima()
# ---------------------------------

@app.route('/clima/<ciudad>')
def get_clima(ciudad):
    """
    Endpoint para obtener el clima de una ciudad.
    (La lógica no cambia, ahora consulta la variable db_clima)
    """
    clima = db_clima.get(ciudad)
    
    if clima:
        return jsonify(clima)
    else:
        return jsonify({"error": "Clima no disponible para esta ciudad"}), 404

if __name__ == '__main__':
    # Ejecuta el servicio en el puerto 5002
    app.run(port=5002, debug=True)