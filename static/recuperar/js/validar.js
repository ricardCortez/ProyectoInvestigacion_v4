  // Agregar el listener para convertir el texto a mayúsculas
  const username = document.querySelector('input[name="usuario"]');
  username.addEventListener('keyup', function() {
    this.value = this.value.toUpperCase();
  });

  function validarFormulario() {
    // Obtener los valores del formulario
    var usuario = document.forms["formularioInicioSesion"]["usuario"].value;
    var contrasena = document.forms["formularioInicioSesion"]["contrasena"].value;

    // Verificar si los campos están vacíos
    if (usuario == "" || contrasena == "") {
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Por favor, complete todos los campos.',
        });
      return false;
    }
    // Agregar cualquier otra validación adicional que necesite aquí

    // Si todo está correcto, enviar el formulario
    return true;
  }