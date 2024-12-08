// Confirmación al atrasar almacenamiento
document.getElementById('atrasar-btn').addEventListener('click', function() {
    if (confirm("¿Estás seguro de que deseas atrasar el almacenamiento?")) {
        document.getElementById('atrasar-form').submit();
    }
});

// Agregar animación de OWL o interactividad para las listas de bienes almacenados
$(document).ready(function() {
    // Crear un efecto de deslizamiento para los bienes almacenados
    $(".bien-info ul").owlCarousel({
        loop: true,
        items: 1,
        nav: true,
        dots: true,
        margin: 10,
        autoplay: true,
        autoplayTimeout: 3000
    });
});