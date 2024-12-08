import Chart from "react-apexcharts";

function HeatMapChart({ data, options }) {
  return (
    <Chart series={data} options={options} type="heatmap" height={350} />
  );
}

export default HeatMapChart;