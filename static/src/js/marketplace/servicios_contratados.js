$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
        items: 3, // Número de tarjetas a mostrar
        loop: true,
        margin: 10,
        nav: true,
        dots: true,
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
});