$(document).ready(function() {
    cargarDatosEstudiantes();
});

function cargarDatosEstudiantes() {
    $('#tabla-asignacion-estudiante tbody').empty();
    $.get("/obtener_usuarios", function(usuarios) {
        $.get("/obtener_secciones_no_asignadas", function(secciones) {
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
        data: {'estudiante_id': usuarioId, 'seccion_id': seccionId},
        type: 'POST',
        success: function(response) {
            alert(response.message);
            cargarDatosEstudiantes();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
