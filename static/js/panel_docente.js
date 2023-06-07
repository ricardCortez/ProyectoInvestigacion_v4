$(document).ready(function() {

// Escucha el evento de clic del enlace "3"
  $("#enlace-link_1").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
    // Agrega aquí el código para cargar el contenido de "link 3"
  });

  // Escucha el evento de clic del enlace "1"
  $("#enlace-link_2").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $.ajax({
      url: "/get_attendance_aula",  // La ruta de tu servidor que devuelve el HTML de attendance_aula
      type: "GET",
      success: function(response) {
        $("#campo-dinamico").html(response);

        // Una vez que la respuesta ha sido renderizada en el campo dinámico, puedes escuchar el evento de envío del formulario
        // Escucha el evento de envío del formulario de búsqueda de estudiantes
        $("#student-search-form").on('submit', function(e) {
          e.preventDefault();  // Previene el comportamiento por defecto del formulario

          // Realiza una solicitud AJAX a la ruta de búsqueda de estudiantes en tu servidor
          $.ajax({
            url: "/search_student_aula",
            type: "POST",
            data: $(this).serialize(),  // Serializa los datos del formulario para el envío
            success: function(response) {
              // Muestra los resultados de la búsqueda en "campo-dinamico"
              $("#campo-dinamico").html(response);
            }
          });
        });
      }
    });
  });

  // Escucha el evento de clic del enlace "2"
  $("#enlace-link_3").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"

    $.ajax({
      url: "/get_attendance_laboratorio",  // La ruta de tu servidor que devuelve el HTML de attendance_aula
      type: "GET",
      success: function(response) {
        $("#campo-dinamico").html(response);

        // Una vez que la respuesta ha sido renderizada en el campo dinámico, puedes escuchar el evento de envío del formulario
        // Escucha el evento de envío del formulario de búsqueda de estudiantes
        $("#student-search-form").on('submit', function(e) {
          e.preventDefault();  // Previene el comportamiento por defecto del formulario

          // Realiza una solicitud AJAX a la ruta de búsqueda de estudiantes en tu servidor
          $.ajax({
            url: "/search_student_laboratorio",
            type: "POST",
            data: $(this).serialize(),  // Serializa los datos del formulario para el envío
            success: function(response) {
              // Muestra los resultados de la búsqueda en "campo-dinamico"
              $("#campo-dinamico").html(response);
            }
          });
        });
      }
    });

  });

  // Escucha el evento de clic del enlace "3"
  $("#enlace-link_4").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
    // Agrega aquí el código para cargar el contenido de "link 3"
  });

});
