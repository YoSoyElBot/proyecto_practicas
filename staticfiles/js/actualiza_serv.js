document.getElementById('showSolicitados').addEventListener('click', function () {
    filtrarServicios('Solicitado');
});
document.getElementById('showAsignados').addEventListener('click', function () {
    filtrarServicios('Asignado');
});
document.getElementById('showEnAtencion').addEventListener('click', function () {
    filtrarServicios('En Atención');
});

function filtrarServicios(estado) {
    let rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        let estadoColumna = row.cells[4].textContent.trim();
        if (estadoColumna === estado || estado === '') {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
