from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/style.css')
def style():
    return send_file('style.css')

if __name__ == '__main__':
    # Cloud Run inyecta la variable PORT, pero por defecto usa 8080 internamente
    app.run(host='0.0.0.0', port=8080)