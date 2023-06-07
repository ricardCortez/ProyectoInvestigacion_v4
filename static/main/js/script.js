// Obtén una referencia a los botones
var adminBtn = document.getElementById("panel-adm-btn");
var personalBtn = document.getElementById("panel-padm-btn");
var docenteBtn = document.getElementById("panel-docente-btn");

// Obtén una referencia al div del spinner
var spinnerDiv = document.getElementById("loading-spinner");

// Agrega un controlador de eventos para cada botón
adminBtn.addEventListener("click", function() {
  mostrarSpinner();
  setTimeout(function() {
    window.location.href = "/logadm";
  }, 2000); // 3 segundos de espera antes de redirigir
});

personalBtn.addEventListener("click", function() {
  mostrarSpinner();
  setTimeout(function() {
    window.location.href = " "; // Redirige a la página deseada
  }, 2000); // 3 segundos de espera antes de redirigir
});

docenteBtn.addEventListener("click", function() {
  mostrarSpinner();
  setTimeout(function() {
    window.location.href = "/docente";
  }, 2000); // 3 segundos de espera antes de redirigir
});

// Función para mostrar el spinner
function mostrarSpinner() {
  // Agrega la clase "active" al div del spinner
  spinnerDiv.classList.add("active");
}

// Manejar el evento pageshow para ocultar el spinner al retroceder la página
window.addEventListener("pageshow", function(event) {
  if (event.persisted) {
    // La página se está mostrando desde el caché (se retrocedió)
    spinnerDiv.classList.remove("active");
  }
});
