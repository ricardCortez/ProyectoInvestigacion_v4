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

      console.log("Nombre de la sección:", seccion.nombre_seccion); // Imprimir el nombre de la sección
    });

    seccionSeleccionada = selectElement.val(); // Actualizar la sección seleccionada inicialmente
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
          .append($("<td>").text(asistencia.fecha))
          .append($("<td>").text(asistencia.numero_cubiculo))
          .append($("<td>").html('<button type="button" class="btnEditarCubiculo" onclick="editarCubiculo(this)">Editar</button>'));

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


function editarCubiculo(button) {
  var fila = $(button).closest("tr");
  var numeroCubiculo = fila.find("td:eq(4)").text();

  fila.find("td:eq(4)").empty();
  var inputField = $("<input>")
    .attr("type", "text")
    .attr("class", "inputCubiculo")
    .val(numeroCubiculo);
  fila.find("td:eq(4)").append(inputField);

  var editarButton = fila.find(".btnEditarCubiculo");
  editarButton.text("Actualizar");
  editarButton.attr("onclick", "actualizarCubiculo(this)");
}

function actualizarCubiculo(button) {
  var fila = $(button).closest("tr");
  var codigoAlumno = fila.find("td:eq(0)").text(); // Obtener el código de alumno de la fila
  var nuevoCubiculo = fila.find(".inputCubiculo").val();

  // Realizar la solicitud POST para enviar el nuevo valor del cubículo
  $.post("/actualizar_cubiculo", { codigo_alumno: codigoAlumno, nuevo_numero_cubiculo: nuevoCubiculo }, function(response) {
    if (response.success) {
      fila.find("td:eq(4)").text(nuevoCubiculo);

      var editarButton = fila.find(".btnEditarCubiculo");
      editarButton.text("Editar");
      editarButton.attr("onclick", "editarCubiculo(this)");
    }
  });
}

function limpiarVistaAsistencia() {
  var tablaAsistencia = $("#tabla_asistencia tbody");

  // Vaciar la tabla actual
  tablaAsistencia.empty();
}
