document.addEventListener('DOMContentLoaded', function() {
  var registrarBtn = document.getElementById('registrar-btn');
  registrarBtn.addEventListener('click', function() {
    var tipoPerfil = document.getElementById('tipo-perfil').value;
    var tipoDocumento = document.getElementById('tipo-documento').value;
    var numeroDocumento = document.getElementById('numero-documento').value;
    var nombre = document.getElementById('nombre').value;
    var apellidoPaterno = document.getElementById('apellido-paterno').value;
    var apellidoMaterno = document.getElementById('apellido-materno').value;
    var correoElectronico = document.getElementById('correo-electronico').value;
    var celular = document.getElementById('celular').value;
    var sexo = document.getElementById('sexo').value;
    var fechaNacimiento = document.getElementById('fecha-nacimiento').value;
    var claveAsignada = document.getElementById('clave-asignada').value;

    // Validar si se han completado todos los campos del formulario
    if (tipoPerfil === '' || tipoDocumento === '' || numeroDocumento === '' || nombre === '' ||
        apellidoPaterno === '' || apellidoMaterno === '' || correoElectronico === '' ||
        celular === '' || sexo === '' || fechaNacimiento === '' || claveAsignada === '') {
      Swal.fire({
        icon: 'error',
        title: 'Complete los datos',
        text: 'Por favor complete todos los campos del formulario.',
      });
      return;
    }

    // Envía los datos al servidor
    fetch('/registro', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'tipo_perfil': tipoPerfil,
        'tipo_documento': tipoDocumento,
        'numero_documento': numeroDocumento,
        'nombre': nombre,
        'apellido_paterno': apellidoPaterno,
        'apellido_materno': apellidoMaterno,
        'correo_electronico': correoElectronico,
        'celular': celular,
        'sexo': sexo,
        'fecha_nacimiento': fechaNacimiento,
        'clave_asignada': claveAsignada
      }),
    })
    .then(response => response.text())
    .then(data => {
      Swal.fire({
        icon: 'success',
        title: 'Registro exitoso',
        text: 'Los datos se han registrado correctamente.',
      });

      // Restablecer los campos del formulario
      document.getElementById('tipo-perfil').value = '';
      document.getElementById('tipo-documento').value = '';
      document.getElementById('numero-documento').value = '';
      document.getElementById('nombre').value = '';
      document.getElementById('apellido-paterno').value = '';
      document.getElementById('apellido-materno').value = '';
      document.getElementById('correo-electronico').value = '';
      document.getElementById('celular').value = '';
      document.getElementById('sexo').value = '';
      document.getElementById('fecha-nacimiento').value = '';
      document.getElementById('clave-asignada').value = '';
    })
    .catch(error => console.error('Error:', error));
  });
});
