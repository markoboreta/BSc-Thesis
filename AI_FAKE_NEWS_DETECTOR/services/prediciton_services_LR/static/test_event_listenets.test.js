global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;
const $ = require('jquery');
global.$ = global.jQuery =$; 

const { JSDOM } = require('jsdom');
const { handleOpenPopUp, handleCLosePopUp, handleOptional, handleSubmit, fetchDataAndDrawChart, showOptionalResults, setupChartToggle} = require('../../common/static/ajaxScript');
const { drawChart } = require('../../common/static/ChartScripts');
jest.mock('../../common/static/ChartScripts', () => ({
  //fetchDataAndDrawChart: jest.fn(() => Promise.resolve({ Fake: 10, Real: 20 })),
  drawChart: jest.fn(),
}));
const axios = require('axios');
const testArticle = "The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.";

const badArticle = "Bad article";


// Mocks and setups specific to jQuery
$.ajax = jest.fn().mockResolvedValue({ success: true });
describe('Unit Test Event Listeners with jQuery', () => {
  beforeEach(() => {
    // Set up the HTML structure for the tests
    $('body').html(`
      <textarea id="area"></textarea>
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
    const dialogElement = $('#resultPopup')[0];
    //fetchDataAndDrawChart: jest.fn(() => Promise.resolve({ Fake: 10, Real: 20 })),
    
    dialogElement.showModal = jest.fn(); // Mock showModal
    dialogElement.close = jest.fn(); // Mock close

    
    global.Chart = function() {
      return {
        destroy: jest.fn()
      };
    };

    $('#submitBtn').on('click', function() {
      handleOpenPopUp($('#resultPopup')[0]); 
    });

    $('.close-popup').on('click', function() {
      handleCLosePopUp($('#resultPopup')[0], $('#optional'), $('#expand-result')[0]);
    });

    $("#expand-result").on('click', function() {
      $("#optional").toggleClass("expanded");
      $("#expand-result").text("Hide other model responses")

    })

  });
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('handleSubmit triggers on submit button click with correct form data', async () => 
  {
    $('#area').val(testArticle);
    const formData = new FormData();
    formData.append('message', $('#area').val().trim());

    const mockResponse = { result: "Predicted Result" }; // why does this work ? 
    $.ajax = jest.fn().mockResolvedValue(mockResponse);
    
    $('#submitBtn').on('click', (e) => {
      handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData, "#main-result");
    });
    $('#submitBtn').trigger('click');
    await new Promise(process.nextTick); // Ensure all promises resolve

    expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
      url: "http://127.0.0.1:5001/predict_LR",
      type: 'POST',
      data: formData
    }));
    expect($("#main-result").text()).toBe(mockResponse.result); // correct rendering
    
  });


  test('handleOptional triggers on submit button click with correct form data', async () => 
  {
    $('#area').val("The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.");
    const formData = new FormData();
    formData.append('message', $('#area').val().trim());

    $("#expand-result").on('click', (e) => {
      handleOptional(e, "http://127.0.0.1:5001/LR/get_result", formData);
    });
    $("#expand-result").trigger('click');
    await new Promise(process.nextTick); // Ensure all promises resolve

    expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
      url: "http://127.0.0.1:5001/LR/get_result",
      type: 'POST',
      data: formData
    }));
  });

  test('handleOpenPopUp is triggered when submit is successful', async () => {
    $('#submitBtn').click();
  
    await new Promise(r => setTimeout(r, 100)); 
  
    expect($('#resultPopup')[0].showModal).toHaveBeenCalled();
  });


  test('handleSubmit triggers on submit button click with incorrect form data', async () => 
    {
      $('#area').val("The law earmarks roughly $60 billion in aid for Ukraine, $26 billion.");
      const formData = new FormData();
      formData.append('message', $('#area').val().trim());
  
      $('#submitBtn').on('click', (e) => {
        handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData);
      });
      $('#submitBtn').trigger('click');
      await new Promise(process.nextTick); // Ensure all promises resolve
      expect($('#error-message').text()).toContain("Text needs to be between 900 and 3000 characters long.");
    });

  
  test('handleCLosePopUp is triggered when close button is clicked', async () => {
    $('.close-popup').trigger('click');
    await new Promise(r => setTimeout(r, 100));
    await new Promise(process.nextTick);
    expect($('#resultPopup')[0].close).toHaveBeenCalled();
  });
  

  test('handleOptional toggles content and updates text on expand/collapse button click', async () => {
    $('#area').val(testArticle);
    
    const mockResponse = { result: "Predicted Result" };
    $.ajax = jest.fn().mockResolvedValue(mockResponse);
    const ro = "#optional1";
    const rt = "#optional2";
    
    $('#submitBtn').on('click', (e) => {
      handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData, mainResult);
    });
    $('#expand-result').trigger('click'); 

    await new Promise(r => setTimeout(r, 100));
    await new Promise(process.nextTick); 
 
    expect($('#optional').hasClass('expanded')).toBeTruthy();
    expect($('#expand-result').text()).toBe("Hide other model responses");
    expect($('optional1').text()).toBe("")
  });



  


  test('Toggle the visibility of the graph section and update button text', async () => {
    const mockChartInstance = { destroy: jest.fn() };
    drawChart.mockReturnValue(mockChartInstance); 
    
    

    const mockResponse = { Fake: 10, Real: 20 }; // why does this work ? 
    $.ajax = $.ajax = jest.fn().mockResolvedValue(mockResponse);
    // First click is supposed to expand and show chart
    $("#countPlotBtn").on("click", async function (event) {
      setupChartToggle("#countPlotBtn","#optional-graphs", "http://127.0.0.1:5001/getTFData", "myChart", "Generate Class Ratio", "Hide graph")
    });
    $('#countPlotBtn').trigger('click');
    await new Promise(r => setTimeout(r, 100));
    
    // Expectations after expansion
    expect($('#optional-graphs').css('display')).not.toBe('none');
    expect($.ajax).toHaveBeenCalledWith("http://127.0.0.1:5001/getTFData");
    expect(drawChart).toHaveBeenCalledTimes(1);
  
    // Second click is supposed to hide and destroy chart
    $('#countPlotBtn').trigger('click');
    await new Promise(r => setTimeout(r, 100)); // Wait for asynchronous actions to complete
  
    expect($('#optional-graphs').css('display')).toBe('none');
    expect(mockChartInstance.destroy).toHaveBeenCalledTimes(1); // Check if the chart destroy method was called
  });
});





// Integration testing
test('handleSubmit triggers on submit button click with correct form data (integration test)', async () => {
  $('#area').val(testArticle);
  const formData = new FormData();
  formData.append('message', $('#area').val().trim());
  axios.post = jest.fn().mockResolvedValue({ data: { result: "Predicted Result" } });

  $('#submitBtn').on('click', async (e) => {
    e.preventDefault();
    const response = await axios.post("http://127.0.0.1:5001/predict_LR", formData);
    $('#main-result').text(response.data.result);
  });

  $('#submitBtn').trigger('click');
  await new Promise(process.nextTick); // Ensure all promises resolve

  expect(axios.post).toHaveBeenCalledWith("http://127.0.0.1:5001/predict_LR", formData);
  expect($("#main-result").text()).toBe("Predicted Result");
  });




