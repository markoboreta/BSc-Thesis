$(document).ready(function () {
  const resultPopup = $("#NB_resultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#expand-result");
  const optionalContent = $("#optional");
  const dialog = $("#NB_resultPopup")[0];
  const optOne = "#optional1";
  const optTwo = "#optional2";
  const mainResult = "#NB-main-result";
  
  // Event listener for submit button click
  $("#submitBtn").on("click", async function (event) {
    event.preventDefault();
    const form = $("#lrForm")[0];
    const LRformData = new FormData(form);      
    //LRformData.append('message', area.val().trim());
    storeFormData(submitBtn, 'LRformData', LRformData);
    NBformData.append('message', area.val().trim());
    console.log(NBformData);

    if(await handleSubmit(event, "http://127.0.0.1:5002/predict_NB", NBformData, mainResult))
    {
      handleOpenPopUp(dialog)
      area.val('');
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

  expandResultBtn.on("click", async function (event) {
    URL = "http://127.0.0.1:5002/NB/get_result";
    showOptionalResults(event, optionalContent, expandResultBtn, URL, NBformData)
  });

  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5002/getNBData", "myChart", "Generate Class Ratio", "Hide graph")
  });
  
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5002/getWCData", "wcChart", "Generate Word Count", "Hide graph")
  });
});


