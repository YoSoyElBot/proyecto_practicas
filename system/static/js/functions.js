
function mostrarSeccion(seccion) {
    // Ocultar todas las secciones
    document.querySelectorAll('.seccion-servicios').forEach(el => {
        el.style.display = 'none';
    });
    // Mostrar la sección seleccionada
    document.getElementById(seccion).style.display = 'block';
}


function mostrarModalFinalizar(servicioId) {
    const form = document.getElementById('formFinalizar');
    form.action = `/finalizar/${servicioId}/`; // URL corregida
    const modal = new bootstrap.Modal(document.getElementById('modalFinalizar'));
    modal.show();
}

function mostrarModalAsignar(servicioId) {
    const form = document.getElementById('formAsignar');
    form.action = `/asignar/${servicioId}/`; // URL corregida
    const modal = new bootstrap.Modal(document.getElementById('modalAsignar'));
    modal.show();
}



function mostrarDetalles(servicioId) {
    fetch(`/detalles_servicio/${servicioId}/`) // Asegúrate de que esta URL es correcta
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red');
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('detallesServicio').innerHTML = html;
            const modal = new bootstrap.Modal(document.getElementById('modalDetalles'));
            modal.show();
        })
        .catch(error => console.error('Error:', error));
}



// Mostrar Mis Servicios por defecto
document.addEventListener('DOMContentLoaded', function() {
    mostrarSeccion('mis-servicios');
});

