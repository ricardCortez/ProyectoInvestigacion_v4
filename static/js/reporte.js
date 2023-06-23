$(document).ready(function() {
  // Obtener la lista de estudiantes y sus secciones mediante una petición AJAX
  $.ajax({
    url: '/get_students_sections',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      // Recorrer los datos obtenidos y construir la tabla
      data.forEach(function(estudiante) {
        var row = '<tr>' +
          '<td>' + estudiante.codigo_alumno + '</td>' +
          '<td>' + estudiante.nombre + '</td>';

        if (estudiante.secciones.length > 0) {
          var secciones = estudiante.secciones.map(function(seccion) {
            return '<li>' + seccion + '</li>'; // Modificación aquí
          }).join('');

          row += '<td><ul>' + secciones + '</ul></td>';
        } else {
          row += '<td>No secciones asignadas</td>';
        }

        row += '</tr>';

        $('tbody').append(row);
      });
    },
    error: function() {
      console.log('Error al obtener la lista de estudiantes y secciones.');
    }
  });
});
