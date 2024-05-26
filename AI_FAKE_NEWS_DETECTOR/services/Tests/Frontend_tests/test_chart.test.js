global.TextEncoder = require("util").TextEncoder;
global.TextDecoder = require("util").TextDecoder;
const $ = require("jquery");
global.$ = global.jQuery = $;
const { JSDOM } = require("jsdom");
const { setupChartToggle } = require("../../common/static/ajaxScript");
const { Chart } = require("chart.js");
let mockChartInstance;
//$.ajax = jest.fn().mockResolvedValue({ success: true });
describe("Unit Test Event Listeners with jQuery", () => {
  beforeAll(() => {
    // Mock the entire Chart module
    global.Chart = jest.fn().mockImplementation(() => ({
      destroy: jest.fn(),
      update: jest.fn(),
      getChart: jest.fn()
    }));
  });
  beforeEach(() => {

    $("body").html(`
      <div id="error-message"></div>
      <button type="button" id="countPlotBtn" class="submit-button">Generate Class Ratio</button>
      <div id="optional-graphs" class="graph">
        <canvas id="myChart" width="400" height="400"></canvas>
        <p id="data-context"></p>
      </div>
    `);

    jest.mock("../../common/static/ChartScripts", () => ({
      drawChart: require("../../common/static/ChartScripts").drawChart,
    }));
    jest.spyOn(window, "Chart").mockImplementation();
    // ajax mock
    jest.spyOn($, "ajax").mockImplementation((options) => {
      return new Promise((resolve, reject) => {
        if (options.url === "http://127.0.0.1:5001/getTFData") {
          resolve({ Fake: 10, Real: 20 });
        } else {
          console.error("Mock AJAX call failed");
          return Promise.reject(new Error("Failed to fetch data"));
        }
      });
    });
    $.ajax({
      url: "http://127.0.0.1:5001/getTFData",
      success: function (data) {
        console.log("AJAX success received data:", data);
      },
      error: function (error) {
        console.error("AJAX error:", error);
      },
    });
  });
  afterEach(() => {
    jest.clearAllMocks();
  });

  test("Toggle the visibility of the graph section and update button text", async () => {
    let btn = 0;
    $("#countPlotBtn").on("click", async function () {
      setupChartToggle(
        "#countPlotBtn",
        "#optional-graphs",
        "http://127.0.0.1:5001/getTFData",
        "myChart",
        "Generate Class Ratio",
        "Hide Graph",  
        btn);
      btn+=1;
    });
    $("#countPlotBtn").trigger("click");
    await new Promise((resolve) => setTimeout(resolve, 100));
    expect(window.Chart).toHaveBeenCalled();

    $("#countPlotBtn").trigger("click");
    await new Promise((resolve) => setTimeout(resolve, 100)); 

    expect($("#countPlotBtn").text()).toBe("Generate Class Ratio");
    expect($("#optional-graphs").css("display")).toBe("none");
  });
});
