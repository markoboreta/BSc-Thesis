// Import the text-encoding polyfill
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;
const $ = require('jquery');
global.$ = $; 
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const { navigateToPage, fetchDataAndDrawChart, makePrediction } = require('../ajaxScript');



describe('navigateToPage function', () => {
  test('should call $.ajax with the correct URL LR', () => {
    // Mock the $.ajax function
    $.ajax = jest.fn();

    navigateToPage('http://127.0.0.1:5001/LR_page');
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: 'http://127.0.0.1:5001/LR_page',
        type: 'GET',
      })
    );
  });
});


describe('navigateToPage function', () => {
  test('should call $.ajax with the correct URL NB', () => {
    // Mock the $.ajax function
    $.ajax = jest.fn();

    navigateToPage('http://127.0.0.1:5002/NB_page');
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: 'http://127.0.0.1:5002/NB_page',
        type: 'GET',
      })
    );
  });
});

describe('navigateToPage function', () => {
  test('should call $.ajax with the correct URL PA', () => {
    // Mock the $.ajax function
    $.ajax = jest.fn();

    navigateToPage('http://127.0.0.1:5003/PA_page');
    expect($.ajax).toHaveBeenCalledWith(
      expect.objectContaining({
        url: 'http://127.0.0.1:5003/PA_page',
        type: 'GET',
      })
    );
  });
});


describe('navigateToPage function error handling', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });
  test('should call $.ajax with the incorrect URL, receive error', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    const ajaxMock = jest.fn().mockImplementation((options) => {
      options.error({ status: 404 }, 'Not Found');
    });
    global.$ = { ajax: ajaxMock };
    navigateToPage('http://127.0.0.1:5003/aad_page');
    expect(ajaxMock).toHaveBeenCalledWith(
      expect.objectContaining({
        url: 'http://127.0.0.1:5003/aad_page',
        type: 'GET',
      })
    );
    // Verify that the error handling function was called
    expect(consoleSpy).toHaveBeenCalledWith('Error occurred while making the request.');
    consoleSpy.mockRestore();
  });
});


describe('makePrediction', () => {
   test('should call $.ajax with the correct arguments on success', async () => {
    const endpointUrl = "http://127.0.0.1:5001/predict_LR";
    const formData = new FormData();
    formData.append('message', "The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.");
    const mockResponse = { result: "The news article is highly likely to be fake according to LR." };

    // Mock the $.ajax function to resolve
    //$.ajax.mockResolvedValue(mockResponse);

    const result = await makePrediction(event,endpointUrl, formData);
    expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
      url: endpointUrl,
      type: 'POST',
      data: formData,
    }));
    expect(result).toEqual(mockResponse);
  });
});

/// REVIEW this test later








