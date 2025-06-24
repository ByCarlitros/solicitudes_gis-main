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

    // Configuración del Gráfico de Barras
    if (typeof labels !== "undefined" && typeof trabajo_propio !== "undefined" && typeof trabajo_apoyo !== "undefined" &&
        typeof trabajo_porcentual_propio !== "undefined" && typeof trabajo_porcentual_apoyo !== "undefined" && 
        typeof total_apoyo_tareas !== "undefined") {
        
        const ctx1 = document.getElementById("puntajePorProfesionalChart").getContext("2d");

        const datosAbsolutos = {
            labels: labels,
            datasets: [
                {
                    label: "Solitudes asignada como profesional",
                    data: trabajo_propio,
                    backgroundColor: "rgba(3, 28, 143, 0.58)",
                    borderColor: "rgb(17, 86, 235)",
                    borderWidth: 1
                },
                {
                    label: "Tareas Internas completadas",
                    data: total_tareas,
                    backgroundColor: "rgba(30, 106, 229, 0.38)",
                    borderColor: "rgb(32, 98, 203)",
                    borderWidth: 1
                },
                {
                    label: "Solitudes asignada como apoyo",
                    data: trabajo_apoyo,
                    backgroundColor: "rgba(14, 174, 6, 0.53)",
                    borderColor: "rgb(9, 127, 3)",
                    borderWidth: 1
                },
                {
                    label: "Tareas Internas como apoyo",
                    data: total_apoyo_tareas,
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
                        beginAtZero: false,
                        ticks: {
                            callback: function (value) {
                                if (value === 1 || value === 10 || value === 100 || value === 1000 || value === 10000 || value === 100000) {
                                    return value;
                                }
                                return '';
                            }
                        }
                    }
                },
                plugins: {
                    legend: { display: true },
                    tooltip: { enabled: true }
                }
            }
        });
    }
});
