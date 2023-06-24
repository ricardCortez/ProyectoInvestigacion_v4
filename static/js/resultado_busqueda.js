$(document).ready(function() {
  var usuarioId = $("#seccion").data("usuario-id");  // Almacena el ID de sesión en una variable global

  console.log("ID del usuario fuera:", usuarioId);

  cargarSecciones(usuarioId);

  $("#student-search-form").submit(function(e) {
    e.preventDefault();

    var codigo_alumno = $("#codigo_alumno").val();
    var seccion_id = $("#seccion").val();  // Aquí se cambia para tomar el id de la sección

    $.post("/search_student_aula", { codigo_alumno: codigo_alumno, seccion: seccion_id })  // Aquí se envía el id de la sección
      .done(function(data) {
        $("#campo-dinamico").html(data);
        var mensaje = data.pertenece_seccion ? "El alumno pertenece a la sección seleccionada." : "El alumno no pertenece a la sección seleccionada.";
        $("#mensaje-seccion").text(mensaje);

        // Obtener la ruta de la primera imagen del directorio correspondiente al usuario
        if (data.registro_rostro && data.registro_rostro.length > 0) {
          var rutaDirectorio = data.registro_rostro[0].ruta_rostro;
          var rutaImagen = rutaDirectorio + "/" + codigo_alumno + "_0.jpg";
          console.log("Ruta de la imagen:", rutaImagen);
          $("#myImage").attr("src", rutaImagen);
        } else {
          console.log("No se encontraron imágenes para el usuario");
        }

        // Log de la ruta del código de alumno buscado
        console.log("Ruta del código de alumno:", rutaDirectorio);
      })
      .fail(function() {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Error en la búsqueda',
        });
      });
  });
});

// Resto del código...

function cargarSecciones(usuarioId) {
  console.log("ID del usuario dentro:", usuarioId);

  $.get("/obtener_secciones", function(secciones) {
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
  });
}