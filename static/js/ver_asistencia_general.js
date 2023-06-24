$(document).ready(function() {
  cargarSecciones();

  $("#search-btn").click(function() {
    var seccionId = $("#seccion").val();

    $.get("/get_students_by_section", { seccion: seccionId })
      .done(function(data) {
        var tbody = $("#estudiantes");
        tbody.empty();  // Limpiar la tabla antes de añadir nuevos datos

        data.estudiantes.forEach(function(estudiante) {
          var row = '<tr>' +
            '<td>' + estudiante.codigo_alumno + '</td>' +
            '<td>' + estudiante.nombre + '</td>' +
            '</tr>';

          tbody.append(row);
        });
      })
      .fail(function() {
        console.log('Error al obtener los estudiantes de la sección.');
      });
  });
});

function cargarSecciones() {
  $.get("/get_all_sections")
    .done(function(secciones) {
      var selectElement = $("#seccion");

      // Vaciar el menú desplegable actual
      selectElement.empty();

      secciones.forEach(function(seccion) {
        // Crear una nueva opción y agregarla al menú desplegable
        var optionElement = $("<option>")
          .val(seccion.id)
          .text(seccion.nombre_seccion);

        selectElement.append(optionElement);
      });
    })
    .fail(function() {
      console.log('Error al obtener todas las secciones.');
    });
}
