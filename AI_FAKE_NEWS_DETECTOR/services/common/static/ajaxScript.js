// Function for navigation buttons
function navigateToPage(url) {
  console.log("Navigating to: ", url);
  $.ajax({
    url: url,
    type: "GET",
    success: function () {
      console.log("Response: You have succsessfuly loaded the LR page!");
      window.location.href = url;
    },
    error: function () {
      console.error("Error occurred while making the request.");
      // Handle error gracefully, e.g., show an error message
    },
  });
}


// Event listeners for navigation buttons, same on every html page
$(document).ready(function () {
  $("#mainPageBtn").click(async function (event) {
    event.preventDefault();
     navigateToPage("http://127.0.0.1:5000/");
  });

  // Event listener for LR page navigation
  $("#lrPageBtn").click(async function (event) {
    event.preventDefault();
    navigateToPage("http://127.0.0.1:5001/LR_page");
  });

  // Event listener for NB page navigation
  $("#nbPageBtn").click(async function (event) {
    event.preventDefault();
     navigateToPage("http://127.0.0.1:5002/NB_page");
  });

  $("#paPageBtn").click(async function (event) {
    event.preventDefault();
    navigateToPage("http://127.0.0.1:5003/PA_page");
  });
});


// Function to handle prediction button, this will send artticle and get result
async function makePrediction(endpointUrl, formData) {
  const timeout = 15000; // 15 seconds
  return $.ajax({
    url: endpointUrl,
    type: "POST",
    data: formData,
    contentType: false,
    processData: false,
    timeout: timeout,
    success: function (data) {
      return data;
    },
    error: function (xhr, status, errorThrown) {
      console.log("AJAX Error:", status, errorThrown, xhr.responseText);
      if (status === "timeout") {
        throw new Error(
          "Request timed out after 15 seconds. Please try again."
        );
      } else {
        throw new Error("Prediction request failed: " + (xhr.responseText || errorThrown || "Unknown error"));
      }
    },
  });
}

// Function to display error message
function displayAlert(message, alertClass, divString) {
  // Create alert element
  const alertElement = $("<div>").addClass("alert " + alertClass).text(message);
  const closeButton = $("<strong>").addClass("close").html("&times;");
  // Append close button to alert element
  alertElement.append(closeButton);

  // Append alert element to error message div
  const errorMessageDiv = $(divString);
  errorMessageDiv.empty().append(alertElement);

  // Event listener for close button click
  // Maybe remove the timer???? 
  closeButton.on("click", function () {
    alertElement.addClass("fade-out"); // Apply fade-out animation
    setTimeout(function () {
      alertElement.remove();
    }, 500); 
  });
}

// Fetching the data to draw the chart
async function fetchDataAndDrawChart(endpointUrl) {
  try {
    const data = await $.ajax({
      url: endpointUrl,
      method: "GET",
      dataType: "json",
    });

    return data;
  } catch (error) {
    displayAlert(
      "An error occurred while processing the data needed for the graph.",
      "alert-warning",
      "#error-message"
    );
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


// Function to close the PopUp 
function closeDialog(dialogElement) {
  if (dialogElement && typeof dialogElement.close === "function") {
    dialogElement.close(); // Close the dialog
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
  $(idName).text(""); 

}

// Function to handle the optional button
async function handleOptional(event, optionalURL, formData) {
  event.preventDefault();
  let activeRequests = 0;

  if (activeRequests > 0) {
    console.log("A request is already in progress. Please wait.");
    return; 
  }
  activeRequests += 1;
  try {
    const res = await makePrediction(optionalURL, formData);
    const message1 = res.result.result1.result;
    const message2 = res.result.result2.result;
    $("#optional1").text(message1);
    $("#optional2").text(message2);
  } catch (error) {
    displayAlert(
      "An error occurred while processing the data.",
      "alert-warning",
      "#error-message-optional"
    );
    console.error("Error:", error);
  } finally {
    activeRequests -= 1;
  }
  console.log(activeRequests);
}

// Fucntion to handle submit button 
async function handleSubmit(event, mainurl, formData) {
  event.preventDefault();
  const textarea = $("#area");
  const text = textarea.val().trim();
  const minLength = 900;
  const maxLength = 3000;

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
    const [lrResult] = await Promise.all([makePrediction(mainurl, formData)]);
    $("#main-result").text(lrResult.result);
    console.log(lrResult)
    return 1;
  } catch (error) {
    displayAlert(
      "An error occurred while processing the data.",
      "alert-warning",
      "#error-message"
    );
    console.error("Error:", error);
  }
}



function handleCLosePopUp(dialog, optionalContent, expandResultBtn)
{
  if (dialog && typeof dialog.close === "function") {
    
    // close the optional if open
    if(optionalContent.hasClass("expanded"))
    {
      optionalContent.toggleClass("expanded");
      expandResultBtn.text("View how other models have responded")
      resetDialogContent("#main-result");
      resetDialogContent("#optional1");
      resetDialogContent("#optional2");
    }
    dialog.close();
  } else {
    console.error("The close method is not supported.");
    // Fallback to hide the dialog
    if (dialog) {
      dialog.style.display = "none";
    }
  }
}


function handleOpenPopUp(dialog)
{
  if (dialog && typeof dialog.showModal === "function") {
    dialog.showModal(); // Show the dialog as a modal
  } else {
    console.error("The showModal method is not supported.");
    // Fallback to display the dialog
    if (dialog) {
      dialog.style.display = "block";
    }
  }
}


//export {handleSubmit,handleOptional,fetchDataAndDrawChart,makePrediction,navigateToPage,handleCLosePopUp,handleOpenPopUp};
