// Pasar el ID del usuario al modal de eliminación
document.addEventListener('DOMContentLoaded', function() {
    var eliminarModal = document.getElementById('eliminarModal');
    eliminarModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget;
        var usuarioId = button.getAttribute('data-id');
        var inputUsuarioId = eliminarModal.querySelector('#usuario_id');
        inputUsuarioId.value = usuarioId;
    });
});
