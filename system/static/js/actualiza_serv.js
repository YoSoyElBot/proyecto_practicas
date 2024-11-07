document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('showAbiertos').addEventListener('click', function() {
        document.getElementById('serviciosAbiertos').style.display = 'block';
        document.getElementById('serviciosCerrados').style.display = 'none';
    });

    document.getElementById('showCerrados').addEventListener('click', function() {
        document.getElementById('serviciosAbiertos').style.display = 'none';
        document.getElementById('serviciosCerrados').style.display = 'block';
    });
});
