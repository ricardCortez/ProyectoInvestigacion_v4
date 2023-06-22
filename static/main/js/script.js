// Obtén una referencia a los botones
var adminBtn = document.getElementById("panel-adm-btn");
var personalBtn = document.getElementById("panel-padm-btn");
var docenteBtn = document.getElementById("panel-docente-btn");

// Agrega un controlador de eventos para cada botón
adminBtn.addEventListener("click", function() {
  localStorage.setItem('rol', 'Administrador');
  window.location.href = "/logadm";
});

personalBtn.addEventListener("click", function() {
  localStorage.setItem('rol', 'Personal administrativo');
  window.location.href = "/logadm";
});

docenteBtn.addEventListener("click", function() {
  localStorage.setItem('rol', 'Docente');
  window.location.href = "/logadm";
});

// Función para establecer el rol seleccionado
function setRolSeleccionado(rol) {
  $.ajax({
    type: 'POST',
    url: '/set-rol',
    data: {
      'rol': rol
    },
    success: function() {
      // Redirige al usuario al formulario de inicio de sesión después de establecer el rol seleccionado
      window.location.href = "/logadm";
    }
  });
}
