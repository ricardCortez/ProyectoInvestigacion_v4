$(document).ready(function() {
  // Escucha el evento de envío del formulario
  $("#miFormulario").submit(function(event) {
    event.preventDefault(); // Evita el envío por defecto

    // Obtiene los valores de los campos
    var nombre = $("#nombre").val();
    var correo = $("#correo").val();
    var contrasena = $("#contrasena").val();

    // Hace una solicitud AJAX al servidor para obtener el campo dinámico
    $.ajax({
      url: "/obtener_campo_dinamico",
      type: "POST",
      data: { nombre: nombre, correo: correo, contrasena: contrasena },
      success: function(respuesta) {
        $("#campo-dinamico").html(respuesta);
      }
    });
  });

  // Escucha el evento de clic del botón de búsqueda
  $("#btnBusqueda").click(function() {
    var busqueda = $("#busqueda").val();

    // Hace una solicitud AJAX al servidor para buscar los datos relacionados al nombre
    $.ajax({
      url: "/buscar_usuario",
      type: "POST",
      data: { busqueda: busqueda },
      success: function(respuesta) {
        $("#campo-dinamico").html(respuesta);
        // Limpia los campos después de la búsqueda exitosa
        $("#busqueda").val("");
        $("#nombre").val("");
        $("#correo").val("");
        $("#contrasena").val("");
      }
    });
  });
});
