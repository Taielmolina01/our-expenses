import { scaleLinear } from 'd3-scale';

// Crear la escala lineal
const colorScale = scaleLinear()
  .domain([0, 30])
  .range(["#00A100", "#FF0000"]);

const colorArray = Array.from({ length: 30 }, (_, i) => colorScale(i));

export function GetChartOptions(typeChart, graphic, chartData) {
  const theme = localStorage.getItem('theme') || 'dark';

  let color = 'white'; // Usar la variable CSS para el color del texto

  if (theme === 'light') {
    color = 'black';
  }

  const chartOptions = typeChart === 'Heatmap' ? { 
    chart: {
      toolbar: { show: false },
    },
    plotOptions: {
      heatmap: {
        shadeIntensity: 0.5,
        colorScale: {
          ranges: colorArray.map((color, index) => ({
            from: index,
            to: index + 1,  // Rango de 1 en 1 para asegurar que cada color se asigne a un solo valor
            color: color,
          })),
        },
      },
    },
    dataLabels: {
      enabled: true,
      style: {
        colors: [color],
      },
    },
    xaxis: {
      title: {
        text: graphic === "Categories by groups" ? 'Categories' : 'Creditors (by name)',
        style: {
          color: color, // Usar la variable CSS para el color del texto
          fontSize: '14px',
        },
      },
      labels: {
        style: {
          colors: color, // Usar la variable CSS para el color de las etiquetas
          fontSize: '12px',
        },
      },
      axisBorder: {
        show: true,
        color: color, // Usar la variable CSS para el color del borde
        width: [2],
      },
      min: 0,
      max: 30,
      categories: chartData.categories,
    },
    yaxis: {
      title: {
        text: graphic === "Categories by groups" ? 'Groups' : 'Debtors (by name)',
        style: {
          color: color, // Usar la variable CSS para el color del texto
          fontSize: '14px',
        },
      },
      labels: {
        style: {
          colors: color, // Usar la variable CSS para el color de las etiquetas
          fontSize: '12px',
        },
      },
      axisBorder: {
        show: true,
        color: color, // Usar la variable CSS para el color del borde
        width: 2,
      },
      min: 0,
      max: 30,
      forceNiceScale: true,
    },
    legend: {
      show: false, // Ocultar la leyenda
    },
    tooltip: {
      callbacks: {
        label: function (tooltipItem) {
          const value = tooltipItem.raw;
          return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        },
      },
    },
  } : {
    responsive: true,
    layout: {
      padding: { top: 20, right: 20, bottom: 20, left: 20 },
    },
    plugins: {
      legend: {
        display: typeChart === 'Bar' ? false : true,
        position: 'bottom',
        labels: {
          color: color, // Usar la variable CSS para el color del texto
          font: {
            size: 14,
          },
        },
      },
      tooltip: {
        style: {
          color: 'black', // Asegura que el texto del tooltip sea siempre negro
        },
        callbacks: {
          label: function (tooltipItem) {
            const value = tooltipItem.raw;
            return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: (() => {
            switch (graphic) {
              case "Amount by category":
                return "Categories";
              case "Amount by year":
                return "Years";
              case "Amount by groups":
                return "Groups";
              case "Amount owed by groups":
                return "Groups";
              default:
                return undefined;
            }
          })(),
          font: { size: 14 },
        },
        grid: { borderColor: color }, // Usar la variable CSS para el color del borde de la cuadrícula
        ticks: {
          display: graphic !== "Amount by payer",
          color: graphic === "Amount by payer" ? "transparent" : color, // Usar la variable CSS para el color de los ticks
        },
      },
      y: {
        title: {
          display: true,
          text: "Amount",
          font: { size: 14 },
        },
        grid: { borderColor: color }, // Usar la variable CSS para el color del borde de la cuadrícula
        ticks: {
          display: graphic !== "Amount by payer",
          color: graphic === "Amount by payer" ? "transparent" : color, // Usar la variable CSS para el color de los ticks
          callback: graphic === "Amount by payer" ? undefined : function (value) {
            return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
          },
        },
      },
    },    
  };

  return chartOptions;
}

export const CHART_PALETTE = [
  "#E91E63", "#00BCD4", "#FFC107", "#8BC34A", "#673AB7", "#FF5722", 
  "#2196F3", "#9C27B0", "#3F51B5", "#4CAF50", "#F44336", "#CDDC39", 
  "#607D8B", "#009688", "#795548", "#FFC0CB", "#BDB76B", "#FF4500", 
  "#00FA9A", "#6A5ACD", "#FFD700", "#ADFF2F", "#1E90FF", "#DAA520", 
  "#FF00FF", "#40E0D0", "#DC143C", "#7B68EE", "#FFA07A", "#98FB98", 
  "#FF1493", "#87CEFA", "#4682B4", "#EE82EE", "#20B2AA", "#32CD32", 
  "#BA55D3", "#FFA500", "#8A2BE2", "#00CED1"
];
