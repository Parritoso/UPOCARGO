$(document).ready(function() {
    // Inicialización del Carrusel de Servicios
    $(".owl-carousel").owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        items: 3,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            }
        }
    });

    // Buscador interactivo (en tiempo real)
    $('#search').on('input', function() {
        var searchQuery = $(this).val().toLowerCase();
        // Filtrar los servicios en tiempo real (en la página actual)
        $('.service-card').each(function() {
            var serviceText = $(this).text().toLowerCase();
            if (serviceText.indexOf(searchQuery) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Confirmación al contratar servicio adicional
    $('.btn.btn-primary').on('click', function(event) {
        event.preventDefault(); // Prevenir la acción predeterminada
        var serviceUrl = $(this).attr('href');
        if (confirm('¿Estás seguro de que deseas contratar este servicio?')) {
            window.location.href = serviceUrl; // Redirigir al usuario para contratar el servicio
        }
    });
});