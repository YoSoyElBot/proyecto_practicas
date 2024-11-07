$(document).ready(function() {
    // Variable para habilitar el botón con combinación de teclas
    let keyPressCount = 0;

    $(document).keydown(function(event) {
        // Combinación de teclas: Ctrl + Alt + L (puedes cambiarlo)
        if (event.ctrlKey && event.altKey && event.key === 'l') {
            keyPressCount++;
            if (keyPressCount === 1) {
                $('#accessButton').show(); // Mostrar el botón
            }
        }
    });
});
