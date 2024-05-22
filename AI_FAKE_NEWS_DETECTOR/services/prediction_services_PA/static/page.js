$(document).ready(function () {
  const resultPopup = $("#PA_resultPopup");
  const closePopupBtn = $(".close-popup");
  const expandResultBtn = $("#PA_expand_result");
  const optionalContent = $("#optional");
  const dialog = $("#PA_resultPopup")[0];
  let optOne = "#optional1";
  let optTwo = "#optional2";
  let mainResult = "#PA-main-result";
  const submitBtn = $("#PAsubmitBtn");
  
  let cntBtn = 0;
  let wcBtn = 0;

  let area = $("#PA_area");
  let char = $("#char")[0];

  area.on("input", function () {
    let content = this.value.trim();
    char.textContent = content.length + " Characters";
  });

  // Event listener for submit button click
  $("#PAsubmitBtn").on("click", async function (event) {
    event.preventDefault();
    let PAformData = new FormData();
    PAformData. append('message', area.val().trim());
    storeFormData(submitBtn, "PAformData", PAformData);
    console.log(PAformData);
    if (
      await handleSubmit(
        event,
        "http://127.0.0.1:5003/predict_PA",
        PAformData,
        mainResult
      )
    ) {
      handleOpenPopUp(dialog);
    }
  });

  // Event listener for close button click
  closePopupBtn.on("click", function () {
    handleCLosePopUp(
      dialog,
      optionalContent,
      expandResultBtn,
      mainResult,
      optOne,
      optTwo
    );
  });

  // Event listener for dialog close event
  resultPopup.on("close", function () {
    handleCLosePopUp(
      dialog,
      optionalContent,
      expandResultBtn,
      mainResult,
      optOne,
      optTwo
    );
  });

  // Event listener for expand/collapse button click
  expandResultBtn.on("click", async function (event) {
    const formData = retrieveFormData(submitBtn);
    URL = "http://127.0.0.1:5003/PA/get_result";
    showOptionalResults(event, optionalContent, expandResultBtn, URL, formData);
  });

  // event listener for true false graph
  $("#countPlotBtn").on("click", async function (event) {
    setupChartToggle(
      "#countPlotBtn",
      "#optional-graphs",
      "http://127.0.0.1:5003/getPAData",
      "myChart",
      "Generate Class Ratio",
      "Hide graph", cntBtn
    ); 
    cntBtn+=1;
  });

  // event listener for char count graph
  $("#wordCountBtn").on("click", async function (event) {
    setupChartToggle(
      "#wordCountBtn",
      "#optional-mean",
      "http://127.0.0.1:5003/getWCData",
      "wcChart",
      "Generate Word Count",
      "Hide graph", wcBtn
    );
    wcBtn+=1;
  });
});
