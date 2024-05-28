$(document).ready(function () {
  const resultPopup = $("#NBresultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#expand-result");
  const optionalContent = $("#optional");
  const dialog = $("#NBresultPopup")[0];
  let optOne = "#optional1";
  let optTwo = "#optional2";
  let mainResult = "#NB-main-result";
  const submitBtn = $("#submit");
  let cntBtn = 0;
  let wcBtn = 0;
  let area = $("#NBarea");
  let char = $("#char")[0];
  

  countCharacters(area, char);

  // Event listener for submit button click
  $("#submit").on("click", async function (event) {
    event.preventDefault();
    const NBformData = new FormData();      
    NBformData.append('message', $("#NBarea").val().trim());
    storeFormData(submitBtn, 'NBformData', NBformData);
    if(await handleSubmit(event, "http://127.0.0.1:5002/predict_NB", NBformData, "#NB-main-result"))
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

  expandResultBtn.on("click", async function (event) {
    const formData = retrieveFormData(submitBtn, "NBformData");
    const URL = "http://127.0.0.1:5002/NB/get_result";
    //console.log(formData);
    showOptionalResults(event, optionalContent, expandResultBtn, URL, formData, optOne, optTwo)
  });

  // drawing the graphs
  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5002/getNBData", "myChart", "Generate Class Ratio", "Hide graph", cntBtn);
    cntBtn+=1;
  });
  
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5002/getWCData", "wcChart", "Generate Mean Word Count", "Hide graph", wcBtn);
    wcBtn+=1;
  });
});


