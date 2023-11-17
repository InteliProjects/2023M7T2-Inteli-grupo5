import React from "react";
import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

const DistributionChart = () => {
  const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

  const [chartData, setChartData] = useState({
    options: {
      colors: ["#1E3A8A", "#4FBCD7"],
      chart: {
        id: "scatter-chart",
      },
      xaxis: {
        categories: [],
      },
    },
    series: [
      {
        name: "Time to failure - hours",
        data: [],
      },
    ],
  });

  useEffect(() => {
    const userToken = "betinho3";

    const headers = {
      Authorization: `Bearer seu_token_aqui`,
    };

    fetch("http://127.0.0.1:8000/failures_time", { headers })
      .then((response) => response.json())
      .then((data) => {
        const timeToFailure = data.map((item) => ((item.time_to_failure/3600)*24).toFixed(0));

        setChartData((prevChartData) => ({
          ...prevChartData,
          options: {
            ...prevChartData.options,
            xaxis: {
              categories: timeToFailure,
            },
          },
          series: [
            {
              ...prevChartData.series[0],
              data: timeToFailure ,
              name: "Time to failure (hrs)",
            },
            
          ],
        }));
      })
      .catch((error) => console.error("Erro ao buscar dados:", error));
  }, []);

  return (
    <>
      <div className="col-4">
        <Chart
          options={chartData.options}
          series={chartData.series}
          type="area"
          width={500}
        />
      </div>
    </>
  );
};

export default DistributionChart;
