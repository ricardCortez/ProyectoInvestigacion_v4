// Agregar el listener para convertir el texto a mayúsculas
const username = document.querySelector('input[name="usuario"]');
const password = document.querySelector('input[name="contrasena"]');

username.addEventListener('keyup', function() {
  this.value = this.value.toUpperCase();
});

$('form[name="formularioInicioSesion"]').on('submit', function(e) {
  // Evitar que el formulario se envíe de la forma tradicional
  e.preventDefault();

  // Obtener los valores del formulario
  var usuario = username.value;
  var contrasena = password.value;

  // Verificar si los campos están vacíos
  if (usuario === "" || contrasena === "") {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Por favor, complete todos los campos.',
    });
    return;
  }

  // Enviar los datos a tu servidor para la autenticación
  $.ajax({
    type: "POST",
    url: "/login",
    data: {
      'usuario': usuario,
      'contrasena': contrasena
    },
    success: function(data) {
      // Si el inicio de sesión es exitoso, mostrar un mensaje de éxito y redirigir a la página de inicio
      Swal.fire({
        icon: 'success',
        title: 'Inicio de sesión exitoso',
        text: 'Bienvenido!',
        timer: 2000, // Tiempo en milisegundos que se mostrará el mensaje antes de redirigir.
        showConfirmButton: false,
        onClose: () => {
          window.location.href = "/inicio";
        }
      });
    },
    error: function(jqXHR, textStatus, errorThrown) {
      // Si hay un error (es decir, el inicio de sesión no es exitoso), mostrar un error
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Usuario o contraseña incorrecta.',
      });
    }
  });
});
