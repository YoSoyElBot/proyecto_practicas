$(document).ready(function() {
    // Desvanecer y eliminar los mensajes después de 5 segundos
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 5000);
});
