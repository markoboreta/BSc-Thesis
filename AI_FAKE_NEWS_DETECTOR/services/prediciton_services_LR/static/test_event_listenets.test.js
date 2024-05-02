global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;
const $ = require('jquery');
global.$ = $; 
const { JSDOM } = require('jsdom');
const { handleOpenPopUp, handleCLosePopUp, handleOptional, handleSubmit} = require('../../common/static/ajaxScript');
const fs = require('fs');
const path = require('path');

// Load and evaluate the page.js
const pageJsPath = path.resolve(__dirname, './page.js');
const pageJsContent = fs.readFileSync(pageJsPath, 'utf-8');
eval(pageJsContent);



// Mocks and setups specific to jQuery
$.ajax = jest.fn().mockResolvedValue({ success: true });

describe('Event Listeners with jQuery', () => {
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
    `);
    const dialogElement = $('#resultPopup')[0];
    dialogElement.showModal = jest.fn(); // Mock showModal
    dialogElement.close = jest.fn(); // Mock close

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
    $('#area').val("The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.");
    const formData = new FormData();
    formData.append('message', $('#area').val().trim());

    $('#submitBtn').on('click', (e) => {
      handleSubmit(e, "http://127.0.0.1:5001/predict_LR", formData);
    });
    $('#submitBtn').trigger('click');
    await new Promise(process.nextTick); // Ensure all promises resolve

    expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
      url: "http://127.0.0.1:5001/predict_LR",
      type: 'POST',
      data: formData
    }));
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
  
  test('handleCLosePopUp is triggered when close button is clicked', async () => {
    $('.close-popup').trigger('click');
    await new Promise(r => setTimeout(r, 100));
    await new Promise(process.nextTick);
    expect($('#resultPopup')[0].close).toHaveBeenCalled();
  });
  

  test('handleOptional toggles content and updates text on expand/collapse button click', async () => {
    $('#expand-result').trigger('click'); // Simulate click event
    await new Promise(r => setTimeout(r, 100));
    await new Promise(process.nextTick); 
    expect($('#optional').hasClass('expanded')).toBeTruthy();
    expect($('#expand-result').text()).toBe("Hide other model responses");
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


});


