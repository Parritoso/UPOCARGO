$(document).ready(function() {
    // Mostrar/Ocultar el desglose de gastos
    $('#toggle-desglose').on('click', function() {
      var desgloseTable = $('#desglose-gastos');
      desgloseTable.slideToggle();
      if(desgloseTable.hasClass("display")){
        desgloseTable.removeClass("display");
      } else {
        desgloseTable.addClass("display");
      }

      // Cambiar texto del botón según la visibilidad de la tabla
      const text = desgloseTable.hasClass('display') ? 'Ocultar Desglose de Gastos' : 'Ver Desglose de Gastos';
      $(this).text(text);
    });

    // Resaltar enlaces de la mudanza asociada con hover
    $('a').hover(function() {
      $(this).css('text-decoration', 'underline');
    }, function() {
      $(this).css('text-decoration', 'none');
    });

    // Iniciar OWL Carousel si hay más de 3 filas en el desglose
    const gastosRows = $('#desglose-gastos tbody tr').length;
    if (gastosRows > 3) {
      $('#desglose-gastos').owlCarousel({
        loop: true,
        items: 1,
        nav: true,
        dots: true,
        autoplay: true,
        autoplayTimeout: 3000,
        margin: 20
      });
    }
  });