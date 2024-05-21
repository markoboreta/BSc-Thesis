$(document).ready(function () {
  const resultPopup = $("#NB_resultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#expand-result");
  const optionalContent = $("#optional");
  const dialog = $("#NB_resultPopup")[0];
  let optOne = "#optional1";
  let optTwo = "#optional2";
  let mainResult = "#NB-main-result";
  const submitBtn = $("#NBsubmitBtn");
  
  // Event listener for submit button click
  $("#NBsubmitBtn").on("click", async function (event) {
    event.preventDefault();
    const form = $("#nbForm")[0];
    const NBformData = new FormData(form);      
    //LRformData.append('message', area.val().trim());
    storeFormData(submitBtn, 'NBformData', NBformData);
    console.log(NBformData);
    if(await handleSubmit(event, "http://127.0.0.1:5002/predict_NB", NBformData, mainResult))
    {
      handleOpenPopUp(dialog)
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
    const formData = retrieveFormData(submitBtn);
    URL = "http://127.0.0.1:5002/NB/get_result";
    showOptionalResults(event, optionalContent, expandResultBtn, URL, formData)
  });

  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5002/getNBData", "myChart", "Generate Class Ratio", "Hide graph")
  });
  
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5002/getWCData", "wcChart", "Generate Word Count", "Hide graph")
  });
});


