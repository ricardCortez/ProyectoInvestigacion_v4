window.addEventListener('DOMContentLoaded', function() {
  // Obtener el campo de texto del código de alumno detectado
  var codigoAlumnoDetectado = document.querySelector('.form-control-static');

  // Obtener el botón "Buscar alumno"
  var buscarAlumnoButton = document.querySelector('form[action="/search_student_laboratorio"] button[type="submit"]');

  // Deshabilitar el botón al cargar la página si el campo está vacío
  if (!codigoAlumnoDetectado.textContent) {
    buscarAlumnoButton.disabled = true;
  }

  // Habilitar o deshabilitar el botón al cambiar el contenido del campo
  codigoAlumnoDetectado.addEventListener('input', function() {
    buscarAlumnoButton.disabled = !codigoAlumnoDetectado.textContent;
  });

  // Asignar el valor del campo al atributo "value" del botón al enviar el formulario
  var formularioLaboratorio = document.getElementById('formulario_laboratorio');
  formularioLaboratorio.addEventListener('submit', function() {
    buscarAlumnoButton.value = codigoAlumnoDetectado.textContent;
  });
});
