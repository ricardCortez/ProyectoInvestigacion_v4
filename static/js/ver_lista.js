$(document).ready(function() {
    document.querySelectorAll('.actualizar').forEach(function(button) {
        button.addEventListener('click', function(e) {
            const cubiculoCell = e.target.parentElement.parentElement.querySelector('.cubiculo');
            cubiculoCell.setAttribute('contenteditable', 'true');
            cubiculoCell.focus();
            e.target.style.display = 'none';
            e.target.parentElement.querySelector('.guardar').style.display = 'inline';
        });
    });

    document.querySelectorAll('.guardar').forEach(function(button) {
        button.addEventListener('click', function(e) {
            const row = e.target.parentElement.parentElement;
            const cubiculoCell = row.querySelector('.cubiculo');
            cubiculoCell.setAttribute('contenteditable', 'false');
            e.target.style.display = 'none';
            e.target.parentElement.querySelector('.actualizar').style.display = 'inline';

            // Aquí puedes agregar el código AJAX para enviar la actualización al servidor
            const codigo_alumno = row.querySelector('td').innerText;
            const nuevo_numero_cubiculo = cubiculoCell.innerText;

            // Ejemplo de cómo podría ser la llamada AJAX
            $.ajax({
                url: '/actualizar_cubiculo',
                type: 'POST',
                data: {
                    codigo_alumno: codigo_alumno,
                    nuevo_numero_cubiculo: nuevo_numero_cubiculo
                },
                success: function(response) {
                    console.log(response);
                }
            });
        });
    });
});
