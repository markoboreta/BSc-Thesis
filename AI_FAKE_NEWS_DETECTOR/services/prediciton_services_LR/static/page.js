$(document).ready(function () {
  const resultPopup = $("#LR_resultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#LR_expand_result");
  const optionalContent = $("#LR_optional");
  const dialog = $("#LR_resultPopup")[0];
  mainResult = "#LR-main-result";
  optOne = "#optional1";
  optTwo = "#optional2";
  const submitBtn = $("#submitBtn");

  

  // Event listener for submit button click
  $("#submitBtn").on("click", async function (event) {
    event.preventDefault();
    const form = $("#lrForm")[0];
    const LRformData = new FormData(form);      
    //LRformData.append('message', area.val().trim());
    storeFormData(submitBtn, 'LRformData', LRformData);
    if(await handleSubmit(event, "http://127.0.0.1:5001/predict_LR", LRformData, mainResult))
   { 
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
      const formData = retrieveFormData(submitBtn, 'LRformData');
      URL = "http://127.0.0.1:5001/LR/get_result";
      showOptionalResults(event, optionalContent, expandResultBtn, URL, formData);
  });


 
  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5001/getTFData", "myChart", "Generate Class Ratio", "Hide graph")
  });
  
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5001/getWCData", "wcChart", "Generate Word Count", "Hide graph")
  });
});

