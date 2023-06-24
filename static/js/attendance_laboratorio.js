$(document).ready(function() {
  var usuarioId = $("#section_name").data("usuario-id");  // Almacena el ID de sesión en una variable global
  cargarSecciones(usuarioId);
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
        .val(seccion.nombre_seccion)
        .text(seccion.nombre_seccion);

      selectElement.append(optionElement);
    });
  });
}
