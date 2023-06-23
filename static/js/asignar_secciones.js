$(document).ready(function() {
    cargarDatos();
});

    // Agregar evento de clic al botón de limpiar asignaciones
    $("#limpiar-asignaciones-btn").click(function() {
        limpiarAsignaciones();
    });


function limpiarAsignaciones() {
    console.log("Botón de limpiar asignaciones clickeado");
    // Realizar una solicitud AJAX para limpiar las asignaciones
    $.ajax({
        url: '/limpiar_asignaciones',
        type: 'POST',
        success: function(response) {
            alert(response.message);
            cargarDatos();  // Recargar los datos para actualizar la lista de secciones no asignadas
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function cargarDatos() {
  $('#tabla-asignacion').empty();  // Limpiar la tabla antes de recargar los datos
  $.get("/obtener_docentes", function(docentes) {
    $.get("/obtener_secciones_no_asignadas", function(secciones) {
      $.get("/obtener_docentes_asignados", function(docentes_asignados) {
        docentes.forEach(function(docente) {
          var fila = '<tr><td>' + docente.nombre + '</td><td><select id="seccion-' + docente.id + '"';
          fila += '>';

          if (secciones.length === 0) {
            fila += '<option value="">Vacío</option>';
          } else {
            secciones.forEach(function(seccion) {
              fila += '<option value="' + seccion.id + '">' + seccion.nombre_seccion + '</option>';
            });
          }

          fila += '</select></td><td>';
          if (secciones.length === 0) {
            fila += '<button disabled>Asignar</button>';
          } else {
            fila += '<button onclick="asignarDocente(' + docente.id + ')">Asignar</button>';
          }
          fila += '</td></tr>';
          $('#tabla-asignacion').append(fila);
        });
      });
    });
  });
}



function asignarDocente(profesorId) {
    var seccionId = $("#seccion-" + profesorId).val();
    $.ajax({
        url: '/asignar_docente',
        type: 'POST',
        data: {
            profesor_id: profesorId,
            seccion_id: seccionId
        },
        success: function(response) {
            alert(response.message);
            cargarDatos();  // Recargar los datos para actualizar la lista de secciones no asignadas
        },
        error: function(error) {
            console.log(error);
        }
    });
}