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

