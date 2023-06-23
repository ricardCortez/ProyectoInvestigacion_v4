$(document).ready(function() {
  var usuarioId = $("#seccion").data("usuario-id");  // Almacena el ID de sesión en una variable global

  console.log("ID del usuario fuera:", usuarioId);

  cargarSecciones(usuarioId);

  $("#student-search-form").submit(function(e) {
    e.preventDefault();

    var codigo_alumno = $("#codigo_alumno").val();
    var seccion = $("#seccion").val();

    $.post("/search_student_aula", { codigo_alumno: codigo_alumno, seccion: seccion })
      .done(function(data) {
        $("#campo-dinamico").html(data);
        var mensaje = data.pertenece_seccion ? "El alumno pertenece a la sección seleccionada." : "El alumno no pertenece a la sección seleccionada.";
        $("#mensaje-seccion").text(mensaje);
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

function cargarSecciones(usuarioId) {
  console.log("ID del usuario dentro:", usuarioId);

  $.get("/obtener_secciones", function(secciones) {
    var selectElement = $("#seccion");

    // Vaciar el menú desplegable actual
    selectElement.empty();

    secciones.forEach(function(seccion) {
      // Verificar si la sección está asociada al docente actual
      if (seccion.profesores && seccion.profesores.some(function(profesor) {
        return profesor.id === usuarioId;
      })) {
        // Crear una nueva opción y agregarla al menú desplegable
        var optionElement = $("<option>")
          .val(seccion.id)
          .text(seccion.nombre_seccion);

        selectElement.append(optionElement);
      }
    });
  });
}
