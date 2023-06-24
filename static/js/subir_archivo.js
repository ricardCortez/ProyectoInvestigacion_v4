$(window).on('load', function() {
  $('#uploadForm').on('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var csvFile = $('#csvFile').val();

    if (csvFile === '') {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Por favor, seleccione un archivo CSV.'
      });
      return;
    }

    $('#submitBtn').prop('disabled', true);

    Swal.fire({
      title: 'Subiendo archivo...',
      onBeforeOpen: function() {
        Swal.showLoading();
      },
      allowOutsideClick: false,
      allowEscapeKey: false
    });

    $.ajax({
      url: '/upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.status === 'success') {
          Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: response.message
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: response.message
          });
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Error al subir el archivo: ' + errorThrown
        });
      },
      complete: function() {
        $('#submitBtn').prop('disabled', false);
      }
    });
  });
});
