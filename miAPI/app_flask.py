from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
    <h2>Agregar Usuario</h2>
    <form id="formUsuario">
        ID: <input type="number" id="id" required>
        Nombre: <input type="text" id="nombre" required>
        Edad: <input type="number" id="edad" required>
        <button type="submit">Agregar</button>
    </form>

    <h2>Lista de Usuarios</h2>
    <table border="1">
        <tr><th>ID</th><th>Nombre</th><th>Edad</th><th>Accion</th></tr>
        {% for u in usuarios %}
        <tr>
            <td>{{ u.id }}</td>
            <td>{{ u.Nombre }}</td>
            <td>{{ u.edad }}</td>
            <td><button onclick="eliminar({{ u.id }})">Eliminar</button></td>
        </tr>
        {% endfor %}
    </table>

    <script>
        document.getElementById('formUsuario').addEventListener('submit', e => {
            e.preventDefault();
            fetch('/api/usuarios', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    id: parseInt(document.getElementById('id').value),
                    Nombre: document.getElementById('nombre').value,
                    edad: parseInt(document.getElementById('edad').value)
                })
            }).then(() => location.reload());
        });

        function eliminar(id) {
            if(confirm('Eliminar?')) {
                fetch(`/api/usuarios/${id}`, {method: 'DELETE'})
                .then(() => location.reload());
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        r = requests.get(f"{API_URL}/v1/usuarios/")
        usuarios = r.json().get('usuarios', [])
    except:
        usuarios = []
    return render_template_string(HTML_TEMPLATE, usuarios=usuarios)

@app.route('/api/usuarios', methods=['POST'])
def create():
    r = requests.post(f"{API_URL}/v1/usuarios_op/", json=request.json)
    return jsonify(r.json())

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def delete(id):
    r = requests.delete(f"{API_URL}/v1/usuarios_op/{id}")
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(debug=True, port=5010)