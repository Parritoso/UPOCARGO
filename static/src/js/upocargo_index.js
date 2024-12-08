$(document).ready(function () {
    // Efecto fade-in para los elementos
    $(window).on('load', function () {
        $('#hero').fadeIn(1000);
        $('#services').fadeIn(1500);
        $('#testimonials').fadeIn(2000);
    });

    // Desplazamiento suave para enlaces internos
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        var target = this.hash;
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 1000);
    });

    // Iniciar OWL Carousel para los testimonios
    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        items: 1
    });

    // Efecto hover en los servicios
    $('.service-item').hover(function () {
        $(this).find('i').css('color', '#ff6f61'); // Cambia el color del icono
        $(this).find('h4').css('color', '#ff6f61'); // Cambia el color del título
    }, function () {
        $(this).find('i').css('color', ''); // Resetea el color
        $(this).find('h4').css('color', ''); // Resetea el color del título
    });
});