from flask import Flask, jsonify
from flask_cors import CORS
import json  # 1. Importamos el módulo json

app = Flask(__name__)
CORS(app)

# --- Base de datos desde JSON ---
# 2. Creamos una función para cargar los datos desde el archivo
def cargar_db():
    """
    Lee el archivo JSON y lo carga en memoria.
    """
    # Usamos 'with' para asegurarnos de que el archivo se cierre correctamente
    # 'encoding="utf-8"' es importante para manejar tildes y caracteres especiales
    with open('usuarios.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 3. Cargamos los datos UNA VEZ cuando el servidor se inicia
db_usuarios = cargar_db()
# ---------------------------------

@app.route('/usuarios')
def get_todos_los_usuarios():
    """
    Devuelve el diccionario completo de usuarios (cargado desde el JSON).
    """
    # Devuelve la variable que ya cargamos
    return jsonify(db_usuarios)

@app.route('/usuarios/<id>')
def get_usuario(id):
    """
    Endpoint para obtener la información de UN usuario por su ID.
    """
    # Busca en la variable que ya cargamos
    usuario = db_usuarios.get(id)
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)