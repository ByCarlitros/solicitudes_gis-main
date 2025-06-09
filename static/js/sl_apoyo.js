$(document).on("click", ".apoyo-link", function (event) {
    event.preventDefault();

    var item = JSON.parse($(this).attr("data-item"));
    var protocoloId = item.id;
    var profesionalActual = item.profesional_id ? `${item.profesional_nombre}` : "No asignado";

    $("#protocoloId").text(protocoloId);
    $("#profesionalActual").text(profesionalActual);

    // Llamada AJAX para obtener usuarios disponibles
    $.ajax({
        url: usuarios_disponibles_url,
        type: "GET",
        data: { protocolo_id: protocoloId },
        success: function (response) {
            var container = $("#listaApoyos");
            container.empty();

            response.usuarios.forEach(function (usuario) { });

            $("#apoyoModal").modal("show");
        },
        error: function () {
            alert("Error al obtener usuarios disponibles.");
        }
    });
});

$("#guardarNota").click(function () {
    var protocoloId = $("#protocoloId").text();
    var usuariosSeleccionados = [];
    $(".apoyo-checkbox:checked").each(function () {
        usuariosSeleccionados.push($(this).val());
    });

    if (usuariosSeleccionados.length === 0) {
        alert("Por favor, selecciona al menos un usuario.");
        return;
    }

    $.ajax({
        url: agregar_apoyo_url,
        type: "POST",
        data: {
            protocolo_id: protocoloId,
            usuarios: JSON.stringify(usuariosSeleccionados),
            csrfmiddlewaretoken: csrf_token
        },
        success: function (response) {
            alert("Apoyos agregados con éxito.");
            $("#apoyoModal").modal("hide");
            location.reload();
        },
        error: function () {
            alert("Error al agregar los apoyos.");
        }
    });
});

$(document).on("click", ".nota-link", function (event) {
    event.preventDefault();

    var item = JSON.parse($(this).attr("data-item"));
    var protocoloId = item.id;
    var profesionalActual = item.profesional_id ? `${item.profesional_nombre}` : "No asignado";

    $("#protocoloId_modal").text(protocoloId);
    $("#profesionalActual_modal").text(profesionalActual);

    // Llamada AJAX para obtener usuarios de apoyo
    $.ajax({
        url: apoyo_trabajo_url,
        type: "GET",
        data: { protocolo_id: protocoloId },
        success: function (response) {
            var apoyoContainer = $("#apoyonotas");
            apoyoContainer.empty();

            var numApoyos = response.apoyos.length;
            var sliderValue = numApoyos > 0 ? 50 : 100;

            $("#porcentajeSlider").val(sliderValue);
            $("#porcentajeInput").val(sliderValue);

            if (numApoyos > 0) {
                $("#apoyoSection").show();
                response.apoyos.forEach(function (usuario) {
                    var checked = usuario.ya_agregado ? "checked" : "";
                    apoyoContainer.append(`
                        <div class="form-check">
                            <input class="form-check-input apoyo-checkbox" type="checkbox" value="${usuario.id}" id="usuario_${usuario.id}" ${checked}>
                            <label class="form-check-label" for="usuario_${usuario.id}">
                                ${usuario.first_name} ${usuario.last_name}
                            </label>
                        </div>
                    `);
                });
            } else {
                $("#apoyoSection").hide();
            }

            $("#notaModal").modal("show");
            actualizarPorcentajes(sliderValue);
        },
        error: function () {
            alert("Error al obtener los apoyos del protocolo.");
        }
    });
});

// Sincronizar el slider con el input numérico
$("#porcentajeSlider").on("input", function () {
    var valor = $(this).val();
    $("#porcentajeInput").val(valor);
    actualizarPorcentajes(valor);
});

// Sincronizar el input numérico con el slider
$("#porcentajeInput").on("input", function () {
    var valor = parseInt($(this).val(), 10);
    if (valor < 0) valor = 0;
    if (valor > 100) valor = 100;
    $("#porcentajeSlider").val(valor);
    actualizarPorcentajes(valor);
});

// Función para actualizar la distribución de porcentajes
function actualizarPorcentajes(valor) {
    var numApoyos = $("#apoyonotas .form-check-input:checked").length;
    var totalPersonas = numApoyos + 1;

    if (totalPersonas > 1) {
        var porcentajePorPersona = valor / totalPersonas;
        $("#porcentajeProfesional").text(porcentajePorPersona.toFixed(0) + "%");
        $("#porcentajeApoyo").text(porcentajePorPersona.toFixed(0) + "%");
    } else {
        $("#porcentajeProfesional").text(valor + "%");
        $("#porcentajeApoyo").text("0%");
    }
}

$(document).on("change", ".apoyo-checkbox", function () {
    var sliderValue = $("#porcentajeSlider").val();
    actualizarPorcentajes(sliderValue);
});
