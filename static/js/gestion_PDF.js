// Función para copiar URL
function copiarURL(url) {
    // Obtener el dominio de la página actual
    var dominio = window.location.origin;
    // Agregar el dominio a la URL del PDF
    var urlCompleta = dominio + url;

    // Crear un campo de texto temporal
    var campoTemporal = document.createElement('textarea');
    campoTemporal.value = urlCompleta;

    // Agregar el campo temporal al DOM
    document.body.appendChild(campoTemporal);

    // Seleccionar y copiar el texto en el campo temporal
    campoTemporal.select();
    document.execCommand('copy');

    // Eliminar el campo temporal
    document.body.removeChild(campoTemporal);

    // Mostrar un mensaje de éxito
    alert('URL copiada: ' + urlCompleta);
}

// Función para manejar la vista previa del PDF (si aplica)
document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('PDFForm');
    var input = form.querySelector('input[type="file"]');
    var preview = document.getElementById('previewImage');

    input.addEventListener('change', function (event) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };

            reader.readAsDataURL(input.files[0]);
        } else {
            preview.src = '#';
            preview.style.display = 'none';
        }
    });

    form.addEventListener('submit', function (event) {
        if (!input.files || input.files.length === 0 || !input.files[0]) {
            event.preventDefault(); // Evitar la presentación del formulario si no se selecciona ningún PDF
            alert('Por favor, seleccione un PDF.');
        }
    });
});
