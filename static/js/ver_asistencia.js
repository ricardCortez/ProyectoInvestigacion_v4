$(document).ready(function() {
  cargarSecciones();

  $("#search-btn").click(function() {
    var seccionId = $("#seccion").val();
    var fecha = $("#fecha").val(); // Obtén la fecha seleccionada

    // Si la fecha no se ha seleccionado, muestra un mensaje de alerta y detén la ejecución
    if (!fecha) {
      alert('Por favor selecciona una fecha.');
      return;
    }

    // Envía tanto la ID de la sección como la fecha al servidor
    $.get("/get_students_by_section", { seccion: seccionId, fecha: fecha })
      .done(function(data) {
        var tbody = $("#estudiantes");
        tbody.empty();  // Limpiar la tabla antes de añadir nuevos datos

        if (data && data.estudiantes && data.estudiantes.length > 0) {
          data.estudiantes.forEach(function(estudiante) {
            var row = '<tr>' +
              '<td>' + estudiante.codigo_alumno + '</td>' +
              '<td>' + estudiante.nombre + '</td>' +
              '</tr>';

            tbody.append(row);
          });
        } else {
          alert('No se encontraron estudiantes para la sección y fecha seleccionadas.');
        }
      })
      .fail(function() {
        console.log('Error al obtener los estudiantes de la sección.');
      });
  });
});

function cargarSecciones() {
  $.get("/obtener_secciones", function(secciones) {
    var selectElement = $("#seccion");

    secciones.forEach(function(seccion) {
      var optionElement = $("<option>")
        .val(seccion.id)
        .text(seccion.nombre_seccion);

      selectElement.append(optionElement);
    });
  });
}
