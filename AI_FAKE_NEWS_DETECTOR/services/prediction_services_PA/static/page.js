$(document).ready(function () {
  const resultPopup = $("#PA_resultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#PA_expand_result");
  const optionalContent = $("#optional");
  optOne = "#optional1";
  optTwo = "#optional2";
  mainResult = "#PA-main-result";
  const dialog = $("#PA_resultPopup")[0];


  // Event listener for submit button click
  $("#submitBtn").on("click", async function (event) {
    event.preventDefault();
    const area = $("#PA_area");
    PAformData = new FormData();
    PAformData.append("message", area.val().trim());
    console.log(PAformData);
    if (
      await handleSubmit(event, "http://127.0.0.1:5003/predict_PA", PAformData, mainResult)
    ) {
      handleOpenPopUp(dialog);
    }
  });

  // Event listener for close button click
  closePopupBtn.on("click", function () {
    handleCLosePopUp(dialog, optionalContent, expandResultBtn, mainResult, optOne, optTwo);
  });

  // Event listener for dialog close event
  resultPopup.on("close", function () {
    handleCLosePopUp(dialog, optionalContent, expandResultBtn, mainResult, optOne, optTwo);
  });

   // Event listener for expand/collapse button click
  expandResultBtn.on("click", async function (event) {
    URL = "http://127.0.0.1:5003/PA/get_result";
    showOptionalResults(event, optionalContent, expandResultBtn, URL, PAformData);
  });


  // event listener for true false graph
  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5003/getPAData", "myChart", "Generate Class Ratio", "Hide graph")
    });

  // event listener for char count graph
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5003/getWCData", "wcChart", "Generate Word Count", "Hide graph")
  });
});
