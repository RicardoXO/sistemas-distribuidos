from flask import Flask, jsonify, send_file, request

app = Flask(__name__)

# Base de datos de usuarios y saldos (ejemplo simple)
usuarios_db = {
    "ana@email.com": {"contrasena": "pass123", "nombre": "Ana", "saldo": 500.0},
    "luis@email.com": {"contrasena": "seguro456", "nombre": "Luis", "saldo": 1200.0},
    "sofia@email.com": {"contrasena": "clave789", "nombre": "Sofía", "saldo": 750.0}
}

# Variable global para mantener el estado del usuario logeado
# En una aplicacion real, se usarian tokens de sesion
sesion_usuario_actual = None

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/login', methods=['POST'])
def login():
    global sesion_usuario_actual
    data = request.get_json()
    email = data.get('email')
    contrasena = data.get('contrasena')

    # Verifica las credenciales
    if email in usuarios_db and usuarios_db[email]['contrasena'] == contrasena:
        sesion_usuario_actual = usuarios_db[email]
        return jsonify({"mensaje": "Inicio de sesión exitoso.", "nombre": sesion_usuario_actual['nombre']})
    else:
        return jsonify({"error": "Credenciales inválidas."}), 401

@app.route('/datos_usuario', methods=['GET'])
def get_datos_usuario():
    if not sesion_usuario_actual:
        return jsonify({"error": "No hay usuario logueado."}), 401
    return jsonify({
        "nombre": sesion_usuario_actual['nombre'],
        "saldo": sesion_usuario_actual['saldo']
    })

@app.route('/transaccion', methods=['POST'])
def transaccion():
    global sesion_usuario_actual
    if not sesion_usuario_actual:
        return jsonify({"error": "No hay usuario logueado."}), 401

    data = request.get_json()
    accion = data.get('accion')
    cantidad = data.get('cantidad')

    try:
        cantidad = float(cantidad)
        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser un número positivo."}), 400
    except ValueError:
        return jsonify({"error": "Cantidad inválida."}), 400

    if accion == "depositar":
        sesion_usuario_actual['saldo'] += cantidad
        mensaje = f"Depósito de ${cantidad} exitoso."
    elif accion == "retirar":
        if cantidad > sesion_usuario_actual['saldo']:
            return jsonify({"error": "Fondos insuficientes."}), 400
        sesion_usuario_actual['saldo'] -= cantidad
        mensaje = f"Retiro de ${cantidad} exitoso."
    else:
        return jsonify({"error": "Acción no válida."}), 400

    return jsonify({"mensaje": mensaje, "saldo": sesion_usuario_actual['saldo']})

if __name__ == '__main__':

    app.run(debug=True)
