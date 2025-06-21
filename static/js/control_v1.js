document.addEventListener('DOMContentLoaded', function () {
    // Animación de los contadores
    const counters = document.querySelectorAll('.counter');
    counters.forEach((counter) => {
        const target = +counter.getAttribute('data-target');
        let count = 0;
        const increment = target / 200;

        const updateCount = () => {
            if (count < target) {
                count += increment;
                counter.innerText = Math.ceil(count);

                if (count >= target / 2.5 && !counter.classList.contains('visible')) {
                    counter.classList.add('visible');
                }

                setTimeout(updateCount, 10);
            } else {
                counter.innerText = target;
            }
        };

        updateCount();
    });

    // Gráfico
    if (typeof labels !== "undefined" && typeof trabajo_propio !== "undefined" && typeof trabajo_apoyo !== "undefined" &&
        typeof trabajo_porcentual_propio !== "undefined" && typeof trabajo_porcentual_apoyo !== "undefined" && 
        typeof total_apoyo_tareas !== "undefined") {
        
        const ctx1 = document.getElementById("puntajePorProfesionalChart").getContext("2d");

        // Redondeamos los datos ANTES de pasarlos al gráfico
        const redondearDatos = (data) => data.map(value => Math.round(value));

        const datosAbsolutos = {
            labels: labels,
            datasets: [
                {
                    label: "Solicitudes asignadas como profesional",
                    data: redondearDatos(trabajo_propio),
                    backgroundColor: "rgba(3, 28, 143, 0.58)",
                    borderColor: "rgb(17, 86, 235)",
                    borderWidth: 1
                },
                {
                    label: "Tareas Internas completadas",
                    data: redondearDatos(total_tareas),
                    backgroundColor: "rgba(30, 106, 229, 0.38)",
                    borderColor: "rgb(32, 98, 203)",
                    borderWidth: 1
                },
                {
                    label: "Solicitudes asignadas como apoyo",
                    data: redondearDatos(trabajo_apoyo),
                    backgroundColor: "rgba(14, 174, 6, 0.53)",
                    borderColor: "rgb(9, 127, 3)",
                    borderWidth: 1
                },
                {
                    label: "Tareas Internas como apoyo",
                    data: redondearDatos(total_apoyo_tareas),
                    backgroundColor: "rgba(30, 229, 66, 0.38)",
                    borderColor: "rgb(63, 203, 32)",
                    borderWidth: 1
                },
            ]
        };

        const chart = new Chart(ctx1, {
            type: "bar",
            data: datosAbsolutos,
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        type: 'logarithmic',
                        stacked: true,
                        min: 1,
                        ticks: {
                            callback: function(value) {
                                if (Number.isInteger(value)) {
                                    return value;
                                }
                                return '';
                            },
                            autoSkip: true,
                            maxTicksLimit: 10
                        },
                        afterBuildTicks: function(scale) {
                            const ticks = [];
                            let value = 1;
                            while (value <= scale.max) {
                                ticks.push(value);
                                value *= 10;
                            }
                            scale.ticks = ticks;
                        }
                    }
                },
                plugins: {
                    legend: { display: true },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + Math.round(context.raw);
                            }
                        }
                    }
                }
            }
        });
    }
});
