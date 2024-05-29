//import { countCharacters } from "../../common/static/ajaxScript";

$(document).ready(function () {
  const resultPopup = $("#LRresultPopup");
  const dialog = $("#LRresultPopup")[0];
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#LRexpand");
  const optionalContent = $("#LRoptional");
  const mainResult = "#LR-main-result";
  const optOne = "#optional1";
  const optTwo = "#optional2";
  const submitBtn = $("#submit");
  let countBtn = 0;
  let wcBtn = 0;
  let area = $("#LRarea");
  let char = $("#char")[0];


  // count characters for user
  countCharacters(area, char);

  // Event listener for submit button click
  $("#submit").on("click", async function (event) {
    event.preventDefault();
    let LRformData = new FormData();      
    LRformData.append('message', area.val().trim());
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
      const URL = "http://127.0.0.1:5001/LR/get_result";
      showOptionalResults(event, optionalContent, expandResultBtn, URL, formData, optOne, optTwo);
  });
  
  // class ratio chart
  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5001/getTFData", "myChart", "Generate Class Ratio", "Hide graph", countBtn);
    countBtn+=1;
    //console.log(countBtn);
  });
  
  // Word count chart
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle("#wordCountBtn","#optional-mean", "http://127.0.0.1:5001/getWCData", "wcChart", "Generate Mean Character Count", "Hide graph", wcBtn);
    wcBtn+=1;
  });
});

