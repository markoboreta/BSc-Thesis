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

// testing the data sent to the makePrediciton

// Mocking $.ajax within the test suite
describe('makePrediction function', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should call $.ajax with the correct url and data', async () => {
    const data = `The law earmarks roughly $60 billion in aid for Ukraine, $26 billion for Israel and $8 billion for security in Taiwan and the Indo-Pacific. It also requires ByteDance to sell TikTok within nine months — or a year, if Biden invokes a 90-day extension — or else face a nationwide ban in the U.S. TikTok has already vowed to fight the measure. “This unconstitutional law is a TikTok ban, and we will challenge it in court,” the company wrote in a Wednesday statement on X following Biden’s signing. “This ban would devastate seven million businesses and silence 170 million Americans,” the company added in its statement. TikTok CEO Shou Zi Chew posted a video response to the enactment of the TikTok bill, calling it a “disappointing moment” and reiterating the company’s commitment to challenge it. Despite Biden’s official support of the TikTok bill, his 2024 reelection campaign told NBC News Wednesday that it would continue using the social media platform to reach voters for at least the next year. Notably, the nine-month to one-year deadline for ByteDance allows it to maintain ownership of TikTok through the November election.`;


    const formData = new FormData();
    formData.append('message', data.trim());

    // Mock $.ajax to resolve successfully
    const successResponse = { result: "success" };
    $.ajax = jest.fn(() => Promise.resolve(successResponse));

    const result = await makePrediction("http://127.0.0.1:5001/predict_LR", formData);

    expect($.ajax).toHaveBeenCalledWith(expect.objectContaining({
      url: "http://127.0.0.1:5001/predict_LR",
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      timeout: 15000
    }));

    expect(result).toEqual(successResponse);
  });

  test('should handle timeout error correctly', async () => {
    const errorMessage = "Request timed out after 15 seconds. Please try again.";
    // Mock $.ajax to simulate a timeout error
    $.ajax = jest.fn().mockImplementation(() => Promise.reject({
      statusText: "timeout"
    }));

    await expect(makePrediction("http://127.0.0.1:5001/predict_LR", new FormData()))
      .rejects.toThrow(errorMessage);
  });

  test('should handle generic error correctly', async () => {
    const genericErrorMessage = "Prediction request failed: Error occurred";
    // Mock $.ajax to simulate a generic error
    $.ajax = jest.fn().mockImplementation(() => Promise.reject({
      statusText: "error",
      status: 500,
      responseText: "Error occurred"
    }));

    await expect(makePrediction("http://127.0.0.1:5001/predict_LR", new FormData()))
      .rejects.toThrow(genericErrorMessage);
  });
});

