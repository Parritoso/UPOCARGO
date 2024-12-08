$(document).ready(function() {
    // Mostrar/Ocultar información de empleados
    $('#empleados-toggle').on('click', function() {
      $('.empleados-info ul').toggleClass('hidden');  // Alterna la clase hidden
    });

    // Confirmación al atrasar la mudanza
    $('#atrasar-btn').on('click', function(event) {
      event.preventDefault();
      if (confirm("¿Estás seguro de que deseas atrasar la mudanza?")) {
        $('button[name="action"][value="atrasar"]').closest('form').submit();
      }
    });

    // Confirmación al cancelar la mudanza
    $('#cancelar-btn').on('click', function(event) {
      event.preventDefault();
      if (confirm("¿Estás seguro de que deseas cancelar la mudanza?")) {
        $('button[name="action"][value="cancelar"]').closest('form').submit();
      }
    });
  });