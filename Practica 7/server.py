from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json, os

app = Flask(__name__, static_folder='static')
CORS(app)

DATA_FILE = "tareas.json"

# ---------- Funciones auxiliares ----------
def cargar_tareas():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def guardar_tareas(tareas):
    with open(DATA_FILE, 'w') as f:
        json.dump(tareas, f, indent=4)

# ---------- Endpoints REST ----------
@app.route('/api/tareas', methods=['GET'])
def obtener_tareas():
    return jsonify(cargar_tareas())

@app.route('/api/tareas', methods=['POST'])
def agregar_tarea():
    tareas = cargar_tareas()
    nueva = request.json
    nueva['id'] = (max([t['id'] for t in tareas]) + 1) if tareas else 1
    tareas.append(nueva)
    guardar_tareas(tareas)
    return jsonify({"mensaje": "Tarea agregada", "tarea": nueva}), 201

@app.route('/api/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tareas = cargar_tareas()
    tareas = [t for t in tareas if t['id'] != id]
    guardar_tareas(tareas)
    return jsonify({"mensaje": "Tarea eliminada"}), 200

@app.route('/api/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tareas = cargar_tareas()
    data = request.json
    for t in tareas:
        if t['id'] == id:
            t.update(data)
            break
    guardar_tareas(tareas)
    return jsonify({"mensaje": "Tarea actualizada"}), 200

# ---------- Archivos estáticos ----------
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)