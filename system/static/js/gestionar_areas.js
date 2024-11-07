$(document).ready(function() {
    // Configurar el modal de eliminación para asignar el área seleccionada
    const eliminarModal = $('#eliminarModal');
    
    eliminarModal.on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget); // Botón que activó el modal
        const areaNombre = button.data('id'); // Extraer información del atributo data-id
        const modalInput = $('#area_id'); // Buscar el input oculto en el modal
        modalInput.val(areaNombre); // Asignar el nombre al input
    });
});
