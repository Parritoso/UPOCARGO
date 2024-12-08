// Mostrar y ocultar la contraseña
$(document).ready(function() {
    $('#toggle-password').click(function() {
      var passwordField = $('#password');
      var icon = $(this).find('i');
      if (passwordField.attr('type') === 'password') {
        passwordField.attr('type', 'text');
        icon.removeClass('fa-eye').addClass('fa-eye-slash');
      } else {
        passwordField.attr('type', 'password');
        icon.removeClass('fa-eye-slash').addClass('fa-eye');
      }
    });

    // Validación del formulario antes de enviar
    $('#form-modificar-datos').submit(function(e) {
      var email = $('#email').val();
      var name = $('#name').val();
      var dir = $('#dir').val();
      var telf = $('#telf').val();
      var password = $('#password').val();
      var errorMessage = '';

      // Validación de campos vacíos
      if (!email || !name || !dir || !telf || !password) {
        errorMessage = 'Por favor, complete todos los campos.';
        $('#error-message').text(errorMessage).show();
        e.preventDefault(); // Previene el envío del formulario
      } else {
        $('#error-message').hide();
      }
    });
  });