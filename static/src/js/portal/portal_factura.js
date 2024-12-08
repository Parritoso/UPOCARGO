$(document).ready(function() {
    // Inicializar el OWL Carousel
    $('.owl-carousel').owlCarousel({
      loop: true,            // Hacer que el carrusel sea infinito
      margin: 10,            // Espaciado entre elementos
      nav: true,             // Mostrar las flechas de navegación
      dots: true,            // Mostrar los puntos de navegación
      responsive: {
        0: {
          items: 1            // En pantallas pequeñas (móviles), mostrar 1 item
        },
        600: {
          items: 3            // En pantallas medianas (tabletas), mostrar 3 items
        },
        1000: {
          items: 4            // En pantallas grandes (escritorio), mostrar 4 items
        }
      }
    });

      $('.factura-card').hover(
        function() {
          $(this).css('transform', 'scale(1.05)');
          $(this).css('transition', 'transform 0.3s ease-in-out');
        },
        function() {
          $(this).css('transform', 'scale(1)');
        }
      );
    });