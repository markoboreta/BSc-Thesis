
// Function for navigation buttons
function navigateToPage(url) {
  console.log("Navigating to: ", url);
  $.ajax({
    url: url,
    type: "GET",
    success: function () {
      console.log("Response: You have succsessfuly loaded a web page!");
      window.location.href = url;
    },
    error: function () {
      console.error("Error occurred while making the request.");
    },
  });
}

// Event listeners for navigation buttons, same on every html page
$(document).ready(function () {
  try {
    $("#mainPageBtn").click(async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5000/");
    });
  } catch (error) {
    console.log(error);
  }

  // Event listener for LR page navigation
  try {
    $("#lrPageBtn").click(async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5001/LR_page");
    });
  } catch (error) {
    console.log(error);
  }

  // Event listener for NB page navigation
  try {
    $("#nbPageBtn").click(async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5002/NB_page");
    });
  } catch (error) {
    console.log(error);
  }

  try {
    $("#paPageBtn").click(async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5003/PA_page");
    });
  } catch (error) {
    console.log(error);
  }
});

// handle AJAX for predcition 
async function makePrediction(endpointUrl, formData) {
  const timeout = 15000; // 15 seconds
  try {
    return $.ajax({
      url: endpointUrl,
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      timeout: timeout,
      success: function (data) {
        console.log("Response returned!");
        return data;
      },
      error: function (xhr, status, errorThrown) {
        console.log("AJAX Error:", status, errorThrown, xhr.responseText);
        if (status === "timeout") {
          throw new Error(
            "Request timed out after 15 seconds. Please try again."
          );
        }
      },
    });
  } catch (error) {
    console.error(error);
  }
}

// Function to display error message
function displayAlert(message, alertClass, divString) {
  const alertElement = $("<div>").addClass("alert " + alertClass).text(message);
  const closeButton = $("<strong>").addClass("close").html("&times;");
  alertElement.append(closeButton);

  const errorMessageDiv = $(divString);
  errorMessageDiv.empty().append(alertElement);

  closeButton.on("click", function () {
    alertElement.addClass("fade-out"); // Apply fade-out animation
    setTimeout(function () {
      alertElement.remove();
    }, 500);
  });
}

// Fetching the data to draw the chart
async function fetchChartData(endpointUrl) {
  try {
    const data = await $.ajax({
      url: endpointUrl,
      method: "GET",
      dataType: "json",
    });
    return data;
  } catch (error) {
    console.log(error);
    displayAlert(
      "An error occurred while processing the data needed for the graph.",
      "alert-warning",
      "#error-message"
    );
  }
}

// Showing optional results, will expand when pressed
async function showOptionalResults(event, optionalContent, expandResultBtn, URL, formData, optOne, optTwo)
{
  try{
    optionalContent.toggleClass("expanded");
    if (optionalContent.hasClass("expanded")) {
      //console.log("I am in expanded")
      expandResultBtn.text("Hide other model responses");
      await handleOptional(event, URL, formData, optOne, optTwo);
    } else {
      //console.log("Not expanded")
      expandResultBtn.text("View how other models have responded");
      
    }
  }
  catch(error)
  {
    console.log("Issue showing data, check button again.")
  }
  
}

// Function to open a PopUp windows(HTML Dialog)
function openDialog(dialogElement) {
  if (dialogElement && typeof dialogElement.close === "function") {
    dialogElement.showModal(); // Close the dialog
  } else {
    console.error("The close method is not supported.");
    // Fallback to hide the dialog
    if (dialogElement) {
      dialogElement.style.display = "none";
    }
  }
}


// Function to reset dialog content
function resetDialogContent(idName) {
  //console.log("resetting diagonal");
  $(idName).text("");
}

// Function to handle the optional result button
async function handleOptional(event, optionalURL, formData, optOne, optTwo) {
  event.preventDefault();
  let activeRequests = 0;
  //console.log("Handling optional", formData);
  if (activeRequests > 0) {
    return;
  }
  activeRequests += 1;
  try {
    const res = await makePrediction(optionalURL, formData);
    const message1 = res.result.result1.result;
    const message2 = res.result.result2.result;
    $(optOne).text(message1);
    $(optTwo).text(message2);
  } catch (error) {
    displayAlert(
      "An error occurred while processing the data.",
      "alert-warning",
      "#error-message-optional"
    );
  } finally {
    activeRequests -= 1;
  }
  //console.log(activeRequests);
}

// Fucntion to handle submit button
async function handleSubmit(event, mainurl, formData, mainResult) {
  event.preventDefault();
  const minLength = 900;
  const maxLength = 3000;
  const text = formData.get("message");
 // console.log("Handling submit", formData);
  if (text.length < minLength || text.length > maxLength) {
    event.preventDefault();
    displayAlert(
      "Text needs to be between 900 and 3000 characters long.",
      "alert-warning",
      "#error-message"
    );
    return;
  }
  try {
    const [newResult] = await Promise.all([makePrediction(mainurl, formData)]);
    $(mainResult).text(newResult.result);
    //console.log("Result ", newResult);
    return newResult;
  } catch (error) {
    displayAlert(
      "An error occurred while processing the data.",
      "alert-warning",
      "#error-message"
    );
    console.error("Error:", error);
  }
}
// handle closing of pop up window
function handleCLosePopUp(dialog,optionalContent,expandResultBtn,mainResult,optOne,optTwo) {
  if (dialog && typeof dialog.close === "function") {
    // close the optional if open
    if (optionalContent.hasClass("expanded")) {
      optionalContent.toggleClass("expanded");
      expandResultBtn.text("View how other models have responded");
      resetDialogContent(mainResult);
      resetDialogContent(optOne);
      resetDialogContent(optTwo);
    }
    dialog.close();
  } else {
    console.error("The close method is not supported.");
    if (dialog) {
      dialog.style.display = "none";
    }
  }
}

function handleOpenPopUp(dialog) {
  if (dialog && typeof dialog.showModal === "function") {
    dialog.showModal(); // Show the dialog as a modal
  } else {
    console.error("The showModal method is not supported.");
    if (dialog) {
      dialog.style.display = "block";
    }
  }
}

async function setupChartToggle(buttonId, contentId, fetchUrl, chartId, generateText, hideText, btnCnt) {
  const countPlotBtn = $(buttonId);
  const optionalContent = $(contentId);
  //const oldCtx = document.querySelector(chartId);
  //const oldChart = Chart.getChart(oldCtx);
  let myChart;
  try {
    if(btnCnt == 0)
      {
        let data = await fetchChartData(fetchUrl);
        //console.log("data ", data)
        myChart = drawChart(data, chartId);
        //console.log("drawing charts");
        optionalContent.toggleClass("expanded");
        countPlotBtn.text(hideText);
        optionalContent.show();
      }
      else
      {
        optionalContent.toggleClass("expanded");
        if (optionalContent.hasClass("expanded")) {
          countPlotBtn.text(hideText);
          optionalContent.show();
        
        } else {
          countPlotBtn.text(generateText);
          optionalContent.hide();
        }
      }
      
  } catch (error) {
      console.error("Error in setupChartToggle:", error);
  }
}

// Store and retrieve formData using jQuery's data method
function storeFormData(submitBtn, key, formData) {
  submitBtn.data(key, formData);
}

function retrieveFormData(submitBtn, key) {
  return submitBtn.data(key);
}

function countCharacters(area, char) {
  area.on('input', function () {
    let content = this.value.trim();
    char.textContent = content.length + " Characters";
  });
}



/*
import { drawChart } from './ChartScripts';
export {
  handleSubmit,
  handleOptional,
  fetchChartData,
  makePrediction,
  navigateToPage,
  handleCLosePopUp,
  handleOpenPopUp,
  setupChartToggle,
  showOptionalResults,
  countCharacters,
};*/
