var seccionSeleccionada = ""; // Variable para almacenar la sección seleccionada

$(document).ready(function() {
  var usuarioId = $("#section_name").data("usuario-id");
  cargarSecciones(usuarioId);

  $("#btnCargarAsistencia").click(function(event) {
    event.preventDefault(); // Evitar que se envíe el formulario

    cargarAsistencia();
  });

  $("#section_name").change(function() {
    seccionSeleccionada = $(this).val(); // Actualizar la sección seleccionada
    limpiarVistaAsistencia();
  });
});

function cargarSecciones(usuarioId) {
  console.log("ID del usuario dentro:", usuarioId);

  $.get("/obtener_secciones", function(secciones) {
    var selectElement = $("#section_name");

    // Vaciar el menú desplegable actual
    selectElement.empty();

    secciones.forEach(function(seccion) {
      // Crear una nueva opción y agregarla al menú desplegable
      var optionElement = $("<option>")
        .val(seccion.id.toString()) // Usar el ID de la sección como valor
        .text(seccion.nombre_seccion);

      selectElement.append(optionElement);
    });

    seccionSeleccionada = selectElement.val();
  });
}

function cargarAsistencia() {
  // Obtener el valor de la sección seleccionada (nombre de la sección)
  var seccionSeleccionadaNombre = $("#section_name").val();

  // Obtener el ID de la sección correspondiente al nombre seleccionado
  var seccionSeleccionadaID = obtenerIDSeccion(seccionSeleccionadaNombre);

  // Realizar la solicitud GET para obtener los datos de asistencia
  $.get("/obtener_asistencia_labo", { seccion_id: seccionSeleccionadaID }, function(datosAsistencia) {
    var tablaAsistencia = $("#tabla_asistencia tbody");

    // Vaciar la tabla actual
    tablaAsistencia.empty();

    datosAsistencia.forEach(function(asistencia) {
      // Verificar si la sección de la asistencia coincide con la sección seleccionada
      if (asistencia.seccion_id === seccionSeleccionadaID) {
        var fila = $("<tr>")
          .append($("<td>").text(asistencia.codigo_alumno))
          .append($("<td>").text(asistencia.nombre_alumno))
          .append($("<td>").text(asistencia.hora))
          .append($("<td>").text(asistencia.fecha));

        tablaAsistencia.append(fila);
      }
    });
  });
}

function obtenerIDSeccion(nombreSeccion) {
  var seccionSeleccionadaID = null;

  // Iterar sobre las opciones del menú desplegable para encontrar el ID de la sección correspondiente al nombre seleccionado
  $("#section_name option").each(function() {
    if ($(this).text() === nombreSeccion) {
      seccionSeleccionadaID = $(this).val();
      return false; // Salir del bucle cuando se encuentra el nombre de la sección correspondiente
    }
  });

  return seccionSeleccionadaID;
}

function limpiarVistaAsistencia() {
  var tablaAsistencia = $("#tabla_asistencia tbody");

  // Vaciar la tabla actual
  tablaAsistencia.empty();
}
