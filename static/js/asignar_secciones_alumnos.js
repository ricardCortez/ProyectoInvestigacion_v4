$(document).ready(function() {
    cargarDatosEstudiantes();
});

    // Agregar evento de clic al botón de limpiar asignaciones
    $("#limpiar-asignaciones").click(function() {
        limpiarAsignacionesEstudiantes();
    });


function limpiarAsignacionesEstudiantes() {
    console.log("Botón de limpiar asignaciones clickeado");
    // Realizar una solicitud AJAX para limpiar las asignaciones
    $.ajax({
        url: '/limpiar_asignaciones_estudiantes',
        type: 'POST',
        success: function(response) {
            alert(response.message);
            cargarDatosEstudiantes();  // Recargar los datos para actualizar la lista de secciones no asignadas
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function cargarDatosEstudiantes() {
    $('#tabla-asignacion-estudiante tbody').empty();
    $.get("/obtener_usuarios", function(usuarios) {
        $.get("/obtener_secciones_noasignadas", function(secciones) {
            $.get("/obtener_estudiantes_asignados", function(usuarios_asignados) {
                usuarios.forEach(function(usuario) {
                    var fila = '<tr><td>' + usuario.nombre + '</td><td><select id="seccion-usuario-' + usuario.id + '"';
                    if (usuarios_asignados.includes(usuario.id)) {
                        fila += ' disabled';
                    }
                    fila += '>';
                    secciones.forEach(function(seccion) {
                        fila += '<option value="' + seccion.id + '">' + seccion.nombre_seccion + '</option>';
                    });
                    fila += '</select></td><td><button onclick="asignarUsuario(' + usuario.id + ')"';
                    if (usuarios_asignados.includes(usuario.id)) {
                        fila += ' disabled';
                    }
                    fila += '>Asignar</button></td></tr>';
                    $('#tabla-asignacion-estudiante tbody').append(fila);
                });
            });
        });
    });
}

function asignarUsuario(usuarioId) {
    var seccionId = $("#seccion-usuario-" + usuarioId).val();
    $.ajax({
        url: '/asignar_estudiante',
        type: 'POST',
        data: {
            'estudiante_id': usuarioId,
            'seccion_id': seccionId
        },
        success: function(response) {
            alert(response.message);
            cargarDatosEstudiantes();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
