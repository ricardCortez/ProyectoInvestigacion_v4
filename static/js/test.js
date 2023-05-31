  $(document).ready(function() {
    // Ocultar los formularios al cargar la página
    $("#formulario_agregar").hide();
    $("#formulario-subir-archivo").hide();
    $("#formulario-eliminar-usuarios").hide();
    $("#formulario-buscar").hide();

    // Escucha el evento de clic del enlace "buscar"
    $("#enlace-busqueda").click(function() {
      $("#formulario-buscar").show();
      $("#formulario_agregar").hide();
      $("#formulario-subir-archivo").hide();
    });

    // Escucha el evento de clic del enlace "agregar"
    $("#enlace-formulario-agregar").click(function() {
      $("#formulario_agregar").show();
      $("#formulario-subir-archivo").hide();
      $("#formulario-buscar").hide();
    });

    // Escucha el evento de clic del enlace "subir-archivo"
    $("#enlace-formulario-subir-archivo").click(function() {
      $("#formulario-subir-archivo").show();
      $("#formulario_agregar").hide();
      $("#formulario-buscar").hide();
    });

    // Escucha el evento de clic del botón de subir archivo
    $("#btnSubirArchivo").click(function(event) {
      event.preventDefault(); // Evita el comportamiento predeterminado del formulario
      var archivo = $("#archivo").prop("files")[0];
      if (archivo) {
        var formData = new FormData();
        formData.append("archivo", archivo);
        // Realiza la solicitud AJAX al servidor para subir el archivo
        $.ajax({
            url: "/subir_archivo",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(respuesta) {
                // Muestra una ventana SweetAlert2 con el mensaje de éxito
                Swal.fire({
                    icon: 'success',
                    title: 'Archivo subido',
                    text: respuesta, // Aquí cambia respuesta.texto a solo respuesta
                });
                // Actualiza el campo dinámico con la respuesta del servidor
                $("#campo-dinamico").html(respuesta); // Aquí cambia respuesta.texto a solo respuesta

                // Imprimir respuesta en la consola del navegador
                console.log("Respuesta del servidor: ", respuesta);
            },
            error: function(xhr, status, error) {
                // Muestra una ventana SweetAlert2 con el mensaje de error
                Swal.fire({
                    icon: 'error',
                    title: 'Error al subir el archivo',
                    text: error, // Aquí cambia respuesta.texto a solo error
                });

                // Imprimir respuesta de error en la consola del navegador
                console.log("Error: ", xhr, status, error);
            }
        });
      } else {
        // Muestra una ventana SweetAlert2 indicando que no se ha seleccionado ningún archivo
        Swal.fire({
          icon: 'warning',
          title: 'Archivo no seleccionado',
          text: 'No se ha seleccionado ningún archivo.',
        });
      }
    });
  });