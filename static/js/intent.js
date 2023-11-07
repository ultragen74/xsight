// Sentiment Analysis
const sentimentOptions = {
    series: [55, 67, 83],
    chart: {
        height: 200,
        type: 'radialBar',
    },
    plotOptions: {
        radialBar: {
            dataLabels: {
                name: {
                    fontSize: '22px',
                },
                value: {
                    fontSize: '16px',
                },
                total: {
                    show: true,
                    label: 'Total',
                    formatter: function (w) {
                        // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
                        return 249
                    }
                }
            }
        }
    },
    labels: ['Texture', 'Appearance', 'Flavour'],
};
const sentimentChart = new ApexCharts(document.querySelector("#sentimentAnalysis"), sentimentOptions);
sentimentChart.render();

// Sparc Chart
const sparkChartSocial = {
    chart: {
        id: 'sparkChartSocial',
        group: 'sparks',
        type: 'line',
        height: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            top: 1,
            left: 1,
            blur: 2,
            opacity: 0.2,
        }
    },
    series: [{
        data: [25, 66, 41, 59, 25, 44, 12, 36, 9, 21]
    }],
    stroke: {
        curve: 'smooth'
    },
    markers: {
        size: 0
    },
    grid: {
        padding: {
            top: 20,
            bottom: 10,
            left: 110
        }
    },
    colors: ['#fff'],
    tooltip: {
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function formatter(val) {
                    return '';
                }
            }
        }
    }
}
new ApexCharts(document.querySelector("#sparkChartSocial"), sparkChartSocial).render();

const pieChartOptions = {
    series: [44, 55, 41],
    chart: {
        width: 380,
        type: 'donut',
    },
    colors:['#16a34a', '#ef4444', '#facc15'],
    plotOptions: {
        pie: {
            startAngle: -90,
            endAngle: 270
        }
    },
    dataLabels: {
        enabled: false
    },
    fill: {
        type: 'gradient',
    },
    legend: {
        formatter: function(val, opts) {
            return val + " - " + opts.w.globals.series[opts.seriesIndex]
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};
const pieChart = new ApexCharts(document.querySelector("#pieChart"), pieChartOptions);
pieChart.render();

// Line Chart
const optionsLine = {
    chart: {
        height: 280,
        type: 'line',
        zoom: {
            enabled: false
        },
        dropShadow: {
            enabled: true,
            top: 3,
            left: 2,
            blur: 4,
            opacity: 1,
        }
    },
    stroke: {
        curve: 'smooth',
        width: 2
    },
    colors: ["#3F51B5", '#2196F3'],
    series: [{
        name: "Music",
        data: [1, 15, 26, 20, 33, 27]
    },
        {
            name: "Photos",
            data: [3, 33, 21, 42, 19, 32]
        },
        {
            name: "Files",
            data: [0, 39, 52, 11, 29, 43]
        }
    ],
    title: {
        text: 'Media',
        align: 'left',
        offsetY: 25,
        offsetX: 20
    },
    subtitle: {
        text: 'Statistics',
        offsetY: 55,
        offsetX: 20
    },
    markers: {
        size: 6,
        strokeWidth: 0,
        hover: {
            size: 9
        }
    },
    grid: {
        show: true,
        padding: {
            bottom: 0
        }
    },
    labels: ['01/15/2002', '01/16/2002', '01/17/2002', '01/18/2002', '01/19/2002', '01/20/2002'],
    xaxis: {
        tooltip: {
            enabled: false
        }
    },
    legend: {
        position: 'top',
        horizontalAlign: 'right',
        offsetY: -20
    }
}

const chartLine = new ApexCharts(document.querySelector('#line-adwords'), optionsLine);
chartLine.render();
//  Radial Chart
const optionsCircle4 = {
    chart: {
        type: 'radialBar',
        height: 350,
        width: 380,
    },
    plotOptions: {
        radialBar: {
            size: undefined,
            inverseOrder: true,
            hollow: {
                margin: 5,
                size: '48%',
                background: 'transparent',

            },
            track: {
                show: false,
            },
            startAngle: -180,
            endAngle: 180

        },
    },
    stroke: {
        lineCap: 'round'
    },
    series: [71, 63, 77],
    labels: ['June', 'May', 'April'],
    legend: {
        show: true,
        floating: true,
        position: 'right',
        offsetX: 70,
        offsetY: 240
    },
}
const chartCircle4 = new ApexCharts(document.querySelector('#radialBarBottom'), optionsCircle4);
chartCircle4.render();