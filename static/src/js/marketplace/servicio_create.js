$(document).ready(function() {
    // Validar que el precio base es un número positivo
    $('#crear-servicio-form').submit(function(e) {
        var precioBase = $('#precio_base').val();
        if (precioBase <= 0) {
            e.preventDefault();
            alert("El precio base debe ser un valor positivo.");
        }
    });
});