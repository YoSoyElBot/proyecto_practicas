// gestionar_problemas.js
document.addEventListener('DOMContentLoaded', function() {
    const eliminarModal = document.getElementById('eliminarModal');

    // Agregar un evento para cuando se muestre el modal
    eliminarModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const problemaId = button.getAttribute('data-id'); // Extraer información del atributo data-id
        const modalInput = eliminarModal.querySelector('#problema_id'); // Buscar el input oculto en el modal
        modalInput.value = problemaId; // Asignar el ID al input
    });
});
