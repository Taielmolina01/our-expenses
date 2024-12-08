import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  LineElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie, Bar } from 'react-chartjs-2';
import './myChart.css';
import HeatMapChart from '../heatMapChart/HeatMapChart';
import { GetChartOptions } from "./chartOptions";
import { PrepareDataForPieChart, 
  PrepareDataforBarplotByCategory, 
  PrepareDataforHeatMap, 
  PrepareDataforBarplotByYear,
  PrepareDebtsDataForBarplotByGroup,
  PrepareDataforBarplotByCategoryByGroup,
  PreparePaymentsDataByGroup
 } from "./prepareDataForChart";
import { ViewType } from "../../utils";

ChartJS.register(
  ArcElement, 
  BarElement, 
  LineElement, 
  CategoryScale, 
  LinearScale, 
  Title, 
  Tooltip, 
  Legend 
);

function MyChart({ view, charts, entity, graphic, data }) {
  const chartTypes = {
    bar: Bar,
    pie: Pie,
    heatmap: HeatMapChart,
  };

  const typeChart = charts[entity][graphic];
  const SelectedChart = chartTypes[typeChart.toLowerCase()];

  if (!SelectedChart) {
    return <p>Invalid chart type: {SelectedChart}</p>;
  }

  let chartData;

  if (view === ViewType.GROUP_CHARTS) {
    switch (typeChart) {
      case 'Bar':
        chartData = graphic === 'Amount by category' 
          ? PrepareDataforBarplotByCategory(data) 
          : PrepareDataforBarplotByYear(data);
        break;
      case 'Pie':
        chartData = PrepareDataForPieChart(data);
        break;
      case 'Heatmap':
        chartData = PrepareDataforHeatMap(data);
        break;
      default:
        break;
    }
  } else {
    switch (typeChart) {
      case 'Bar': {
        switch (graphic) {
          case "Amount owed by groups":
            chartData = PrepareDebtsDataForBarplotByGroup(data);
            break;
          case "Amount by groups":
            chartData = PreparePaymentsDataByGroup(data);
            break;
          default:
            break;
        }
        break;
      }
      case 'Heatmap':
        chartData = PrepareDataforBarplotByCategoryByGroup(data);
        break;
      default: 
        break;
    }
  }

  const CHART_OPTIONS = GetChartOptions(typeChart, graphic, chartData);

  return (
    <div className={`chart-container${Object.keys(data).length === 0 ? '-no-data' : ''}`}>
      {Object.keys(data).length === 0 ? (
        entity === "Unpaid debts" ?
        <p style={{margin: "auto", textAlign: 'center'}}> No debts available</p>
        : 
        (entity === "Payments") ?
        <p style={{margin: "auto", textAlign: 'center'}}> No payments available</p>
        :
        <p style={{margin: "auto", textAlign: 'center'}}> No data available</p>
      ) : (
        <SelectedChart 
          data={typeChart === 'Heatmap' ? chartData.series : chartData}
          options={CHART_OPTIONS}
        />
      )}
    </div>
  );
}

export default MyChart;