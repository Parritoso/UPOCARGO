// Función que se ejecuta cuando el DOM se carga
$(document).ready(function () {
    // Efecto Hover en los enlaces de la barra de navegación
    $('.navbar-item').hover(function () {
      $(this).addClass('hovered');
    }, function () {
      $(this).removeClass('hovered');
    });

    // Efecto Hover en el botón de "Modificar mis datos"
    $('.modify-button').hover(function () {
      $(this).addClass('hovered-button');
    }, function () {
      $(this).removeClass('hovered-button');
    });
  });