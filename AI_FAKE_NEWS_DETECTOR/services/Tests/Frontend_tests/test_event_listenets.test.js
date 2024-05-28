global.TextEncoder = require("util").TextEncoder;
global.TextDecoder = require("util").TextDecoder;
const $ = require("jquery");
global.$ = global.jQuery = $;
const { JSDOM } = require("jsdom");
const {
  handleOpenPopUp,
  handleCLosePopUp,
  handleOptional,
  handleSubmit,
  showOptionalResults,
  navigateToPage,
  countCharacters,
} = require("../../common/static/ajaxScript");
const { drawChart } = require("../../common/static/ChartScripts");
const { Chart } = require("chart.js");
const testArticle =
  "The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.";
const wrongArticle = "aaaaaaaaaaa";
const wrongArticle2 = "11 11 11 11";

// Mocks and setups specific to jQuery
$.ajax = jest.fn().mockResolvedValue({ success: true });
describe("Unit Test Event Listeners with jQuery", () => {
  beforeEach(() => { // set up the following operations before each test
    // Set up the HTML structure for the tests
    $("body").html(`
    <button class="navButton" id="lrPageBtn">LR</button>
      <textarea id="area"></textarea>
      <span id="char">0 Characters</span>
      <div id="error-message"></div>
      <input type="submit" id="submitBtn" class="submit-button" value="Submit">
      <dialog id="resultPopup" class="popup">
        <a href="#" class="close-popup">&times;</a>
        <h2>Result</h2>
        <div id="main-result" class="content"></div>
        <button id="expand-result">View how other models have responded</button>
        <div id="optional">
          <div id="optional1" class="optional-content"></div>
          <div id="optional2" class="optional-content"></div>
          <div id="error-message-optional"></div>
        </div>
      </dialog>
      <div id="error-message"></div>
      <button type="button" id="countPlotBtn" class="submit-button">Generate Class Ratio</button>
      <div id="optional-graphs" class="graph">
        <canvas id="myChart" width="400" height="400"></canvas>
        <p id="data-context"></p>
      </div>
    `);
    const dialogElement = $("#resultPopup")[0];
    // Mock console.log and console.error
    console.log = jest.fn(); // mocking console .log
    console.error = jest.fn(); 
    $.ajax = jest.fn(() => $.Deferred().resolve());
    console.log.mockClear();
    console.error.mockClear();

    dialogElement.showModal = jest.fn(); // Mock showModal
    dialogElement.close = jest.fn(); // Mock close
    global.Chart = function () {
      return {
        Chart: jest.fn(),
      };
    };
    global.drawChart = jest.fn();

    // what to do on submission
    $("#submitBtn").on("click", function () {
      handleOpenPopUp($("#resultPopup")[0]);
    });

    // close pop up button on click
    $(".close-popup").on("click", function () {
      handleCLosePopUp(
        $("#resultPopup")[0],
        $("#optional"),
        $("#expand-result")[0],
        $("#main-result"),
        "#optional1",
        "#optional2"
      );
    });
  });
  afterEach(() => {
    jest.clearAllMocks();
  });

    // test submission
  test("handleSubmit triggers on submit button click with correct form data", async () => {
    const formData = new FormData();
    formData.append("message", testArticle.trim());
    const mockResponse = { result: "Predicted Result" }; // mock the result
    $.ajax = jest.fn().mockResolvedValue(mockResponse);

    $("#submitBtn").on("click", (e) => {
      handleSubmit(
        e,
        "http://127.0.0.1:5001/predict_LR",
        formData,
        "#main-result"
      );
    });
    $("#submitBtn").trigger("click");
    await new Promise(process.nextTick); // Ensure all promises resolve
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5001/predict_LR",
        type: "POST",
        data: formData,
      })
    );
    expect($("#main-result").text()).toBe(mockResponse.result); // mock correct text
  });

  

  test("handleOpenPopUp is triggered when submit is successful", async () => {
    $("#submitBtn").click();
    await new Promise((r) => setTimeout(r, 100));
    expect($("#resultPopup")[0].showModal).toHaveBeenCalled();
  });

  test("handleSubmit triggers on submit button click with incorrect form data", async () => {
    const formData = new FormData();
    $.ajax = jest.fn().mockImplementation(() => Promise.reject(new Error("Text needs to be between 900 and 3000 characters long.")));
    formData.append("message", wrongArticle.trim());

    $("#submitBtn").on("click", async (e) => {
      await handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData);
    });
    $("#submitBtn").trigger("click");
    await new Promise(process.nextTick); // Ensure all promises resolve
    expect($("#error-message").text()).toContain(
      "Text needs to be between 900 and 3000 characters long."
    );
  });


  // mock handle optional error
  test("handleOptional triggers on submit button click with incorrect form data", async () => {
    const formData = new FormData();
    formData.append("message", " ");
    $.ajax = jest.fn().mockImplementation(() => Promise.reject(new Error("An error occurred while processing the data.")));
    $("#expand-result").on("click", async (e) => {
      await handleOptional(e, "http://127.0.0.1:5001/LR/get_result", formData);
    });
    $("#expand-result").trigger("click");
    await new Promise(process.nextTick);
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5001/LR/get_result",
        type: "POST",
        data: formData,
      })
    );
    expect($("#error-message-optional").text()).toContain(
      "An error occurred while processing the data."
    );
  });

  
  test("handleSubmit triggers on submit button click with incorrect numerical form data", async () => {
    const formData = new FormData();
    formData.append("message", wrongArticle2.trim());
    $.ajax = jest.fn().mockImplementation(() => Promise.reject(new Error("An error occurred while processing the data.")));
    $("#submitBtn").on("click", (e) => {
      handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData);
    });
    $("#submitBtn").trigger("click");
    await new Promise(process.nextTick); // Ensure all promises resolve
    expect($("#error-message").text()).toContain(
      "Text needs to be between 900 and 3000 characters long."
    );
  });


  test("handleCLosePopUp is triggered when close button is clicked", async () => {
    $(".close-popup").trigger("click");
    await new Promise((r) => setTimeout(r, 100));
    await new Promise(process.nextTick);
    expect($("#resultPopup")[0].close).toHaveBeenCalled();
  });

  test("showOptionalResults toggles content and updates text on expand/collapse button click", async () => {
    const formData = new FormData();
    formData.append("message", testArticle.trim());
    const mockResponseShow = {
      result: {
        result1: { result: "Some result message" },
        result2: { result: "Some other result message" },
      },
    };
    const mockResponseHide = {
      result: {
        result1: { result: "" },
        result2: { result: "" },
      },
    };
    // Mock setup for the first click to show results
    $.ajax = jest.fn().mockResolvedValue(mockResponseShow);
    $("#expand-result").on("click", async (event) => {
      const URL = "http://127.0.0.1:5001/LR/get_result";
      const optionalContent = $("#optional");
      const expandResultBtn = $("#expand-result");
      await showOptionalResults(
        event,
        optionalContent,
        expandResultBtn,
        URL,
        formData,
        "#optional1",
        "#optional2"
      );
    });
    // First click to show results
    $("#expand-result").trigger("click");
    await new Promise((r) => setTimeout(r, 500)); // Ensure all promises resolve
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5001/LR/get_result",
        type: "POST",
        data: formData,
      })
    );
    expect($("#optional1").text()).toBe("Some result message");
    $.ajax.mockResolvedValue(mockResponseHide); 
    // Second click to hide results
    $("#expand-result").trigger("click");
    await new Promise((r) => setTimeout(r, 500)); // Ensure all actions complete
    expect($("#expand-result").text()).toBe(
      "View how other models have responded"
    );
  });

  test("LR Page Button Click Navigates to Correct URL", async () => {
    $("#lrPageBtn").on("click", async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5001/LR_page");
    });
    $("#lrPageBtn").trigger("click");
    await $.ajax();

    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5001/LR_page",
        type: "GET",
      })
    );
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5001/LR_page",
        type: "GET",
      })
    );
  });

  test("LR Page Button Click Handles Error", async () => {
    // Making AJAX call reject
    const consoleSpy = jest.spyOn(console, "error").mockImplementation();
    const ajaxMock = jest.fn().mockImplementation((options) => {
      options.error({ status: 404 }, "Not Found");
    });
    global.$ = { ajax: ajaxMock };
    $("#lrPageBtn").on("click", async function (event) {
      event.preventDefault();
      navigateToPage("http://127.0.0.1:5003/aad_page");
    });
    $("#lrPageBtn").trigger("click");
    await $.ajax();
    expect(ajaxMock).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "http://127.0.0.1:5003/aad_page",
        type: "GET",
      })
    );
    expect(consoleSpy).toHaveBeenCalledWith(
      "Error occurred while making the request."
    );
    consoleSpy.mockRestore();
  });


  test("countCharacters updates character count on text input", () => {
    const textInput = "This is my app";
    const area = $("#area");
    const char = $("#char")[0];
    countCharacters(area, char);
    $("#area").val(textInput).trigger("input"); 
    expect($("#char").text()).toBe(textInput.length + " Characters");
  });

});
