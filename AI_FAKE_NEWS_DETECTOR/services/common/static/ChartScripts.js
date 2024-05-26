// function to draw a chart

function drawChart(data, canvasID) {
  if (!data) {
      console.error("No data provided to drawChart");
      return;
  }
  const labels = Object.keys(data); // labels of chart
  const values = Object.values(data).map(Number); // values of chart

  const dataset = {
      labels: labels, 
      datasets: [{
          label: 'Count', 
          data: values, 
          backgroundColor: [
            labels[0] === "Fake" ? "rgba(255, 99, 132, 0.6)" : "rgba(75, 192, 192, 0.6)",
            labels[1] === "Fake" ? "rgba(255, 99, 132, 0.6)" : "rgba(75, 192, 192, 0.6)", 
          ],
          borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
      }]
  };
  const canvas = document.getElementById(canvasID);
  const ctx = canvas.getContext("2d"); 

  // Create new chart instance
  window.myChart = new Chart(ctx, {
      type: "bar",
      data: dataset,
      options: {
          responsive: false,
          scales: {
              x: {
                title:{
                    display:true,
                    text: "Label",
                    color: "Black"
                }
              },
              y: {
                    title:{
                        display:true,
                        text: "Count",
                        color: "Black"
                    },
                    beginAtZero: true
              }
          }
      }
  });

  return window.myChart;
}

//export{ drawChart }
