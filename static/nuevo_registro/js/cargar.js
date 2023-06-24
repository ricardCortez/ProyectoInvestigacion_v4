document.addEventListener('DOMContentLoaded', function() {
  var registrarBtn = document.getElementById('registrar-btn');
  registrarBtn.addEventListener('click', function() {
    console.log("El botón de registrar ha sido pulsado.");
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

    // Validación de los campos del formulario
    if (!/^[0-9]{8}$/.test(numeroDocumento)) {
      Swal.fire('Error', 'Número de documento inválido. Solo se permiten 8 dígitos.', 'error');
      return;
    }

    if (!/^[A-Za-z\s]+$/.test(nombre)) {
      Swal.fire('Error', 'Nombre inválido. Solo se permiten letras.', 'error');
      return;
    }

    if (!/^[A-Za-z\s]+$/.test(apellidoPaterno)) {
      Swal.fire('Error', 'Apellido Paterno inválido. Solo se permiten letras.', 'error');
      return;
    }

    if (!/^[A-Za-z\s]+$/.test(apellidoMaterno)) {
      Swal.fire('Error', 'Apellido Materno inválido. Solo se permiten letras.', 'error');
      return;
    }

    if (!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(correoElectronico)) {
      Swal.fire('Error', 'Correo Electrónico inválido. Asegúrese de que contiene "@".', 'error');
      return;
    }

    if (!/^[0-9]{9}$/.test(celular)) {
      Swal.fire('Error', 'Número de celular inválido. Solo se permiten 9 dígitos.', 'error');
      return;
    }

    if (fechaNacimiento === '') {
      Swal.fire('Error', 'Seleccione una fecha de nacimiento.', 'error');
      return;
    }

    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/.test(claveAsignada)) {
      Swal.fire('Error', 'Clave asignada inválida. Debe contener al menos una letra mayúscula, un número, un símbolo especial y ser de 6 caracteres.', 'error');
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
