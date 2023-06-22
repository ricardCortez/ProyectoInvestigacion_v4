$("#student-search-form").submit(function(e) {
  e.preventDefault();

  var location = $("#searchLocation").val(); // Obtener el valor seleccionado
  var codigo_alumno = $("#codigo_alumno").val();

  var url = location == "aula" ? "/search_student_aula" : "/search_student_laboratorio"; // Dependiendo de la opción, escoge la ruta correcta

  $.post(url, { codigo_alumno: codigo_alumno }) // Usa el valor seleccionado para determinar la ruta de POST
  .done(function(data) {
    $("#campo-dinamico").empty();
    $("#campo-dinamico").html(data); // Inserta los resultados en el div "campo-dinamico"
  });
});
