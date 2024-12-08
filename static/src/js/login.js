// Inicializar AOS
AOS.init();

$(document).ready(function () {
  // Efecto hover en el botón de login
  $('.login-button').hover(function() {
    $(this).css('background-color', '#ff6f61'); // Cambia el color de fondo del botón
    $(this).css('cursor', 'pointer'); // Cambia el cursor a pointer
  }, function() {
    $(this).css('background-color', ''); // Resetea el color de fondo
  });

  // Mostrar/Ocultar Contraseña
  $('#toggle-password').click(function() {
    var passwordField = $('#password');
    var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
    passwordField.attr('type', type);
    $(this).toggleClass('fa-eye fa-eye-slash');
  });

  // Validación en tiempo real del email
  $('#email').on('input', function() {
    var email = $(this).val();
    var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (emailRegex.test(email)) {
      $(this).css('border-color', 'green');
      $('#email-error').hide();
    } else {
      $('#email-error').show();
      $(this).css('border-color', 'red');
      $('#email-error').text('Correo electrónico no válido.');
    }
  });

  // Validación en tiempo real de la contraseña
  //$('#password').on('input', function() {
    //var password = $(this).val();
    //if (password.length >= 6) {
      //$(this).css('border-color', 'green');
      //$('#password-error').text('');
    //} else {
      //$(this).css('border-color', 'red');
      //$('#password-error').text('La contraseña debe tener al menos 6 caracteres.');
    //}
  //});
});