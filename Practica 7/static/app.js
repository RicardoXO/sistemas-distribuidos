const API_URL = '/api/tareas';
const pendientes = document.getElementById('pendientes');
const completadas = document.getElementById('completadas');
const form = document.getElementById('formulario');
const input = document.getElementById('nuevaTarea');
const estado = document.getElementById('estado');

let modoOffline = false;

//Cargar tareas (del servidor o del almacenamiento local)
async function cargarTareas() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();
    mostrarTareas(data, false);
    localStorage.setItem('tareas', JSON.stringify(data)); // 💾 Guardamos una copia local
    estado.textContent = "🟢 Conectado";
    modoOffline = false;
  } catch {
    const guardadas = JSON.parse(localStorage.getItem('tareas') || "[]");
    mostrarTareas(guardadas, true);
    estado.textContent = "🔴 Sin conexión (solo lectura)";
    modoOffline = true;
  }
}

//Mostrar tareas en pantalla
function mostrarTareas(data, offline = false) {
  pendientes.innerHTML = '';
  completadas.innerHTML = '';

  data.forEach(t => {
    const li = document.createElement('li');
    li.className = t.hecho ? 'hecho' : '';
    li.innerHTML = `
      <label>
        <input type="checkbox" ${t.hecho ? 'checked' : ''} ${offline ? 'disabled' : ''}>
        ${t.titulo}
      </label>
      <button ${offline ? 'disabled' : ''}>🗑️</button>
    `;

    const checkbox = li.querySelector('input');
    const boton = li.querySelector('button');

    if (!offline) {
      checkbox.onchange = () => marcarHecho(t.id, checkbox.checked);
      boton.onclick = () => eliminarTarea(t.id);
    }

    (t.hecho ? completadas : pendientes).appendChild(li);
  });
}

//Agregar nueva tarea
form.onsubmit = async (e) => {
  e.preventDefault();
  if (modoOffline) {
    alert("No puedes agregar tareas sin conexión.");
    return;
  }

  const tarea = { titulo: input.value, hecho: false };
  await fetch(API_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(tarea)
  });
  input.value = '';
  cargarTareas();
};

//Eliminar tarea
async function eliminarTarea(id) {
  await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  cargarTareas();
}

//Marcar tarea como completada
async function marcarHecho(id, hecho) {
  await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ hecho })
  });
  cargarTareas();
}

//Recargar automáticamente al reconectarse
window.addEventListener('online', cargarTareas);
window.addEventListener('offline', () => {
  const guardadas = JSON.parse(localStorage.getItem('tareas') || "[]");
  mostrarTareas(guardadas, true);
  estado.textContent = "🔴 Sin conexión (solo lectura)";
  modoOffline = true;
});

//Inicialización
cargarTareas();

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
