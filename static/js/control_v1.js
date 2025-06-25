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

    // Gráfico de barras con escala logarítmica en Y (vertical)
    if (typeof labels !== "undefined" && typeof trabajo_propio !== "undefined" &&
        typeof trabajo_apoyo !== "undefined" && typeof total_tareas !== "undefined" &&
        typeof total_apoyo_tareas !== "undefined") {

        const ctx = document.getElementById("puntajePorProfesionalChart").getContext("2d");

        const miGrafico = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Solicitudes como Profesional",
                        data: trabajo_propio,
                        backgroundColor: "rgba(3, 28, 143, 0.58)",
                        borderColor: "rgb(17, 86, 235)",
                        borderWidth: 1,
                        hoverBackgroundColor: "rgba(3, 28, 143, 0.8)",
                        hoverBorderColor: "#ffffff",
                        hoverBorderWidth: 2
                    },
                    {
                        label: "Tareas Internas Completadas",
                        data: total_tareas,
                        backgroundColor: "rgba(30, 106, 229, 0.38)",
                        borderColor: "rgb(32, 98, 203)",
                        borderWidth: 1
                    },
                    {
                        label: "Solicitudes como Apoyo",
                        data: trabajo_apoyo,
                        backgroundColor: "rgba(14, 174, 6, 0.53)",
                        borderColor: "rgb(9, 127, 3)",
                        borderWidth: 1
                    },
                    {
                        label: "Tareas como Apoyo",
                        data: total_apoyo_tareas,
                        backgroundColor: "rgba(30, 229, 66, 0.38)",
                        borderColor: "rgb(63, 203, 32)",
                        borderWidth: 1
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    legend: {
                        display: true
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: {
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            size: 13
                        },
                        padding: 10,
                        cornerRadius: 4,
                        displayColors: false
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: function (value) {
                            return value >= 1000 ? value.toLocaleString() : value;
                        },
                        font: {
                            weight: 'bold'
                        },
                        color: '#000'
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        grid: {
                            color: 'rgba(55, 65, 81, 0.5)'
                        }
                    },
                    y: {
                        type: 'logarithmic',
                        stacked: true,
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(55, 65, 81, 0.5)'
                        },
                        ticks: {
                            callback: function (value) {
                                const logValue = Math.log10(value);
                                return Number.isInteger(logValue) ? value.toLocaleString() : '';
                            }
                        }
                    }
                },
                layout: {
                    padding: {
                        left: 20,
                        right: 40,
                        top: 10,
                        bottom: 10
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    }
});
