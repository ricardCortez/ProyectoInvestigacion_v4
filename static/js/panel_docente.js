$(document).ready(function() {

  // Escucha el evento de clic del enlace "1"
  $("#enlace-link_1").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
    // Agrega aquí el código para cargar el contenido de "link 1"
  });

  // Escucha el evento de clic del enlace "2"
  $("#enlace-link_2").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
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

  // Escucha el evento de clic del enlace "3"
  $("#enlace-link_3").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
    $.ajax({
      url: "/get_attendance_laboratorio",  // La ruta de tu servidor que devuelve el HTML de attendance_laboratorio
      type: "GET",
      success: function(response) {
        $("#campo-dinamico").html(response);
      }
    });
  });

  // Escucha el evento de clic del enlace "4"
  $("#enlace-link_4").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
  $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"

    // Cargar las secciones en el menú desplegable
    //cargarSecciones();

      // Realiza una solicitud AJAX a la ruta que devuelve el template "resultados_busqueda.html"
      $.ajax({
        url: '/busqueda_alumnos',  // Asegúrate de reemplazar esto con la ruta correcta
        type: 'GET',
        success: function(data) {
          // En caso de éxito, carga el contenido del template en "campo-dinamico"
          $("#campo-dinamico").html(data);
        },
        error: function(error) {
          // En caso de error, muestra un mensaje
          console.log('Ha ocurrido un error al cargar el template', error);
        }
      });
  });

  // Escucha el evento de clic del enlace "5"
  $("#enlace-link_5").click(function(e) {
      e.preventDefault();  // Previene el comportamiento por defecto del enlace
      $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"

      // Realiza una solicitud AJAX para obtener el contenido del botón "Ver lista asistentes"
      $.ajax({
        url: "/verasistencia",  // La ruta de tu servidor que devuelve el HTML de la lista de asistentes
        type: "GET",
        success: function(response) {
          $("#campo-dinamico").html(response);
        },
        error: function(error) {
          console.log('Ha ocurrido un error al cargar el contenido', error);
        }
      });

  });

  // Escucha el evento de clic del enlace "6"
  $("#enlace-link_6").click(function(e) {
      e.preventDefault();  // Previene el comportamiento por defecto del enlace
      $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"

      // Realiza una solicitud AJAX para obtener el contenido del botón "Ver lista asistentes"
      $.ajax({
        url: "/reporte",  // La ruta de tu servidor que devuelve el HTML de la lista de asistentes
        type: "GET",
        success: function(response) {
          $("#campo-dinamico").html(response);
        },
        error: function(error) {
          console.log('Ha ocurrido un error al cargar el contenido', error);
        }
      });

  });

    // Escucha el evento de clic del enlace "7"
  $("#enlace-link_7").click(function(e) {
    e.preventDefault();  // Previene el comportamiento por defecto del enlace
    $("#campo-dinamico").empty();  // Vacía el contenido de "campo-dinamico"
    // Agrega aquí el código para cargar el contenido de "link 6"
  });

});
