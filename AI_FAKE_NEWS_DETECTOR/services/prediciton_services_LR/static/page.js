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
        formData.append('message', area.val().trim());
        console.log(formData);

    if(await handleSubmit(event, "http://127.0.0.1:5001/predict_LR", formData))
   { 
      console.log("Here should open pop up")
      const dialog = $("#resultPopup")[0];
      handleOpenPopUp(dialog);
    } 
  });

  // Event listener for close button click
  closePopupBtn.on("click", function () {
    const dialog = $("#resultPopup")[0];
    handleCLosePopUp(dialog, optionalContent, expandResultBtn);
  });
  
  // Event listener for dialog close event
  resultPopup.on("close", function () {
    const dialog = $("#resultPopup")[0];
    handleCLosePopUp(dialog, optionalContent, expandResultBtn);
  });

    // Event listener for expand/collapse button click
  expandResultBtn.on("click", async function (event) {
    optionalContent.toggleClass("expanded");
    // Update button text based on content visibility
    if (optionalContent.hasClass("expanded")) {
      expandResultBtn.text("Hide other model responses");
      await handleOptional(event,"http://127.0.0.1:5001/LR/get_result", formData);
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
      const data = await fetchDataAndDrawChart("http://127.0.0.1:5001/getTFData");
      // Ensure the canvas is visible before drawing the chart
      optionalContent.show();
      // Destroy existing chart if it exists
      if (myChart) {
        myChart.destroy();
      }
      // Draw new chart
      myChart = drawChart(data, "myChart");
    } else {
      countPlotBtn.text("Generate Class Ratio");
      // Hide the canvas when collapsing
      optionalContent.hide();
      // Destroy chart when collapsing (optional)
      if (myChart) {
        myChart.destroy();
        myChart = null;
        console.log("Chart destroyed");
        countPlotBtn.text("Generate Class Ratio");
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
      const data = await fetchDataAndDrawChart("http://127.0.0.1:5001/getWCData");
      optionalContent.show();
      // Destroy existing chart if it exists
      if (myChart) {
        myChart.destroy();
      }
      // Draw new chart
      myChart = drawChart(data, "wcChart");
      console.log(myChart)
    } else {
      countPlotBtn.text("Generate Word Cloud");
      // Hide the canvas when collapsing
      optionalContent.hide();
      if (myChart) {
        myChart.destroy();
        myChart = null;
      }
    }
  });
});
