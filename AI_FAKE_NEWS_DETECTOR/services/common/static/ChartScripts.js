function drawChart(data, canvasID) {
  if (!data) {
    console.error("No data provided to drawChart");
    return;
  }
  const labels = Object.keys(data);
  const values = Object.values(data).map(Number); // Convert values to numbers
  // Get canvas element
  const canvas = document.getElementById(canvasID);
  const ctx = document.getElementById(canvasID).getContext("2d");

  const datasets = labels.map((label) => {
    // Determine color based on label
    let backgroundColor =
      label === "Fake" ? "rgba(255, 99, 132, 0.6)" : "rgba(75, 192, 192, 0.6)";
    let borderColor =
      label === "Fake" ? "rgba(255, 99, 132, 1)" : "rgba(75, 192, 192, 1)";

    return {
      label: label,
      data: [data[label]], // Data corresponding to this label
      backgroundColor: backgroundColor,
      borderColor: borderColor,
      borderWidth: 1,
    };
  });
  // Create new chart instance
  const myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Label",
            color: "black",
          },
        },
        y: {
          title: {
            display: true,
            text: "Count",
            color: "black",
          },
          ticks: {
            color: "black",
          },
          beginAtZero: true,
        },
      },
    },
  });
  return myChart;
}
export{ drawChart }