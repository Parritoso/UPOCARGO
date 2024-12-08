// Inicializar AOS
AOS.init();

$(document).ready(function () {
  // Efecto hover en el botón de cambiar contraseña
  $('.login-button').hover(function() {
    $(this).css('background-color', '#ff6f61'); // Cambia el color de fondo del botón
    $(this).css('cursor', 'pointer'); // Cambia el cursor a pointer
  }, function() {
    $(this).css('background-color', ''); // Resetea el color de fondo
  });

  // Mostrar/Ocultar Nueva Contraseña
  $('#toggle-password').click(function() {
    var passwordField = $('#password');
    var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
    passwordField.attr('type', type);
    $(this).toggleClass('fa-eye fa-eye-slash');
  });

  // Mostrar/Ocultar Confirmar Contraseña
  $('#toggle-password-confirm').click(function() {
    var passwordFieldConfirm = $('#password_confirm');
    var type = passwordFieldConfirm.attr('type') === 'password' ? 'text' : 'password';
    passwordFieldConfirm.attr('type', type);
    $(this).toggleClass('fa-eye fa-eye-slash');
  });

  // Validación en tiempo real de la nueva contraseña
  $('#password').on('input', function() {
    var password = $(this).val();
    if (password.length >= 6) {
      $(this).css('border-color', 'green');
      $('#password-error').text('');
      $('#password-error').hide();
    } else {
      $(this).css('border-color', 'red');
      $('#password-error').text('La nueva contraseña debe tener al menos 6 caracteres.');
      $('#password-error').show();
    }
  });

  // Validación en tiempo real de la confirmación de contraseña
  $('#password_confirm').on('input', function() {
    var confirmPassword = $(this).val();
    var password = $('#password').val();
    if (confirmPassword === password) {
      $(this).css('border-color', 'green');
      $('#password-confirm-error').text('');
    } else {
      $(this).css('border-color', 'red');
      $('#password-confirm-error').text('Las contraseñas no coinciden.');
    }
  });
});