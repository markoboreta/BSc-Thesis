$(document).ready(function () {
  const submitBtn = $("#submitBtn");
  const nbForm = $('#lrForm');
  const resultPopup = $("#resultPopup");
  const closePopupBtn = $(".close-popup");
  const countPlotBtn = $("#countPlotBtn");
  const area = $("#area");
  const expandResultBtn = $("#expand-result");
  const optionalContent = $("#optional");
  let activeRequests = 0;

  
  // Event listener for submit button click
  $("#submitBtn").on("click", async function (event) {
    event.preventDefault();

    formData = new FormData();
    formData.append('message', area.val());
    console.log(formData);

    if(await handleSubmit(event, "http://127.0.0.1:5002/predict_NB", formData))
    {
      console.log("Here should open pop up")
      const dialog = $("#resultPopup")[0];
      handleOpenPopUp(dialog)
    }
  });


// Event listener for close button click
closePopupBtn.on("click", function () {
  const dialog = document.getElementById("resultPopup");
  handleCLosePopUp(dialog, optionalContent, expandResultBtn);
});

// Event listener for dialog close event
resultPopup.on("close", function () {
  const dialog = document.getElementById("resultPopup");
  handleCLosePopUp(dialog, optionalContent, expandResultBtn);
});


  // Event listener for expand/collapse button click
  expandResultBtn.on("click", async function (event) {
    optionalContent.toggleClass("expanded");
    // Update button text based on content visibility
    if (optionalContent.hasClass("expanded")) {
      expandResultBtn.text("Hide other model responses");
      await handleOptional(event,"http://127.0.0.1:5002/NB/get_result", formData);
    } else {
      expandResultBtn.text("View how other models have responded");
    }
  });
});


$(document).ready(function () {
  const countPlotBtn = $("#countPlotBtn");
  const optionalContent = $("#optional-graphs");
  let myChart = null;
  countPlotBtn.on("click", async function () {
    optionalContent.toggleClass("expanded");
    if (optionalContent.hasClass("expanded")) {
      countPlotBtn.text("Hide graph");
      const data = await fetchDataAndDrawChart("http://127.0.0.1:5002/getNBData");
      // Ensure the canvas is visible before drawing the chart
      optionalContent.show();
      if (myChart) {
        myChart.destroy();
      }
      // Draw new chart
      myChart = drawChart(data, "myChart");
    } else {
      countPlotBtn.text("Generate graph");
      optionalContent.hide();
      if (myChart) {
        myChart.destroy();
        myChart = null;
        console.log("Chart destroyed");
      }
    }
  });
});


$(document).ready(function () {
  const countPlotBtn = $("#wordCountBtn");
  const optionalContent = $("#optional-mean");
  let myChart = null;
  countPlotBtn.on("click", async function () {
    optionalContent.toggleClass("expanded");
    if (optionalContent.hasClass("expanded")) {
      countPlotBtn.text("Hide graph");
      // Fetch data and draw chart
      const data = await fetchDataAndDrawChart("http://127.0.0.1:5002/getWCData");
      // Ensure the canvas is visible before drawing the chart
      optionalContent.show();
      if (myChart) {
        myChart.destroy();
      }
      myChart = drawChart(data, "wcChart");
      console.log(myChart)
    } else {
      countPlotBtn.text("Generate Word Cloud");
      optionalContent.hide();
      if (myChart) {
        myChart.destroy();
        myChart = null;
      }
    }
  });
});

