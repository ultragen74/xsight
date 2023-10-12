const options = {
    chart: {
        height: 300,
        type: "area"
    },
    dataLabels: {
        enabled: false
    },
    colors:['#9622CB', '#DFB7FF'],
    series: [
        {
            name: "Series 1",
            data: [45, 52, 38, 45, 19, 23, 2]
        }
    ],
    fill: {
        type: "gradient",
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 90, 100]
        }
    },
    xaxis: {
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul"
        ]
    }
};

(async function() {
    const data = [
        { year: 2010, count: 10 },
        { year: 2011, count: 20 },
        { year: 2012, count: 15 },
        { year: 2013, count: 25 },
        { year: 2014, count: 22 },
        { year: 2015, count: 30 },
        { year: 2016, count: 28 },
    ];

    new Chart(
        document.getElementById('acquisitions'),
        {
            type: 'bar',
            data: {
                labels: data.map(row => row.year),
                datasets: [
                    {
                        label: 'Acquisitions by year',
                        data: data.map(row => row.count)
                    }
                ]
            }
        }
    );
})();

const revenueOptions = {
    chart: {
        height: 200,
        type: "area"
    },
    dataLabels: {
        enabled: false
    },
    colors:['#9622CB'],
    series: [
        {
            name: "Series 1",
            data: [50, 52, 58, 65, 69, 75, 80, 85, 90, 108, 112, 120]
        }
    ],
    fill: {
        type: "gradient",
        colors:['#9622CB', '#E91E63', '#9C27B0'],
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 90, 100]
        }
    },
    xaxis: {
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]
    }
};
const revenueChart = new ApexCharts(document.querySelector("#revenueChart"), revenueOptions);
revenueChart.render();
const salesPrediction = {
    series: [{
        data: [50, 52, 58, 65, 69, 75, 80, 85, 90, 108, 112, 120]
    }, {
        data: [50, 52, 58, 65, 69, 75, 80, null, null, null, null, null]
    }],
    chart: {
        height: 251,
        type: 'area',
        toolbar: {
            show: false
        },
    },
    dataLabels: {
        enabled: false
    },
    colors:["#6ee7b7", '#7e22ce'],
    stroke: {
        curve: 'smooth'
    },
    legend: {
        show:false,
    },
    xaxis: {
        categories: [
            "Jan 22",
            "Feb 22",
            "Mar 22",
            "Apr 22",
            "May 22",
            "Jun 22",
            "Jul 22",
            "Aug 22",
            "Sep 22",
            "Oct 22",
            "Nov 22",
            "Dec 22"
        ]
    },
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
};
const predictionChart = new ApexCharts(document.querySelector("#predictionChart"), salesPrediction);
predictionChart.render();
// Stacked bar chart
const barChartOptions = {
    series: [{
        name: 'Net Profit',
        data: [44, 55, 87, 96, 106]
    }],
    chart: {
        type: 'bar',
        height: '256'
    },
    colors:['#9622CB'],
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded',
            borderRadius: 8
        },
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        show: true,
        showForSingleSeries: false,
        position: 'bottom',
        horizontalAlign: 'center',
        labels: {
            colors: ['#7F74AD'],
            useSeriesColors: false
        },
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: ['2018', '2019', '2020', '2021', '2022'],
    },
    fill: {
        opacity: 1
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return "$ " + val + " thousands"
            }
        }
    }
};

const barChart = new ApexCharts(document.querySelector("#barChart"), barChartOptions);
barChart.render();

// Candies Chart - Radial Bar Chart
const radialBarChart = {
    series: [44, 55, 67],
    chart: {
        height: 232,
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
                        // By default, this function returns the average of all series. The below is just an example to show the use of custom formatter function
                        return 166
                    }
                }
            }
        }
    },
    labels: ['Kitkat', 'Snicker', 'Twix'],
};

const radialChart = new ApexCharts(document.querySelector("#radialBarChart"), radialBarChart);
radialChart.render();

// spark Chart Must be like this
const sparcChartOptions = {
    chart: {
        type: 'line',
        height: 40,
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
        data: [12, 14, 2, 47, 32, 44, 14, 55, 41, 69]
    }],
    stroke: {
        curve: 'smooth'
    },
    grid: {
        padding: {
            top: 20,
            bottom: 10,
            left: 110
        }
    },
    markers: {
        size: 0
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
};
const sparcChart = new ApexCharts(document.querySelector("#sparcChart"), sparcChartOptions);
sparcChart.render();


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
const sparkOptions = {
    series: [{
        data: [25, 66, 41, 89, 63]
    }],
    chart: {
        type: 'line',
        width: 100,
        height: 35,
        sparkline: {
            enabled: true
        }
    },
    colors:['#FFFFFF'],
    tooltip: {
        fixed: {
            enabled: false
        },
        x: {
            show: false
        },
        y: {
            title: {
                formatter: function (seriesName) {
                    return ''
                }
            }
        },
        marker: {
            show: false
        }
    }
};

const sparkChart = new ApexCharts(document.querySelector("#sparkChartSocial"), sparkOptions);
sparkChart.render();

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
