  
// Set the dimensions of the SVG container
var margin = { top: 50, right: 20, bottom: 20, left: 40 },
  width = 960 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

// Create SVG container
var svg = d3
  .select("body")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Load data
d3.csv("https://raw.githubusercontent.com/vega/vega/main/docs/data/seattle-weather.csv").then(function(data) {
  // Convert data types
  data.forEach(function(d) {
    d.precipitation = +d.precipitation;
    d.temp_max = +d.temp_max;
    d.temp_min = +d.temp_min;
    d.wind = +d.wind;
  });

  // Define x and y scales
  var xScale = d3
    .scaleBand()
    .domain(
      data.map(function(d) {
        return d.date;
      })
    )
    .range([0, width])
    .padding(0.1);

  var yScale = d3
    .scaleLinear()
    .domain([0, d3.max(data, function(d) { return d.precipitation; })])
    .range([height, 0]);

  // Define x and y axes
  var xAxis = d3.axisBottom(xScale);
  var yAxis = d3.axisLeft(yScale);

  // Define function to draw histogram
  function drawHistogram(data, variable) {
    // Update yScale domain based on selected variable
    yScale.domain([0, d3.max(data, function(d) { return d[variable]; })]);
  
    // Update bars
    var bars = svg.selectAll("rect").data(data);
  
    // Add new bars
    bars
      .enter()
      .append("rect")
      .attr("x", function(d) {
        return xScale(d.date);
      })
      .attr("y", function(d) {
        return yScale(d[variable]);
      })
      .attr("width", xScale.bandwidth())
      .attr("height", function(d) {
        return height - yScale(d[variable]);
      })
      .attr("fill", "red");
  
    // Update existing bars
    bars
      .attr("x", function(d) {
        return xScale(d.date);
      })
      .attr("y", function(d) {
        return yScale(d[variable]);
      })
      .attr("width", xScale.bandwidth())
      .attr("height", function(d) {
        return height - yScale(d[variable]);
      })
      .attr("fill", "blue");
  
    // Remove old bars
    bars.exit().remove();
  
    // Update axes
    svg.select(".x-axis").call(xAxis);
    svg.select(".y-axis").call(yAxis);
  
    // Add histogram label
    svg.selectAll(".histogram-label").remove(); // remove any existing labels
  
    svg
      .append("text")
      .attr("class", "histogram-label")
      .attr("x", width / 2)
      .attr("y", height + margin.bottom - 5)
      .attr("text-anchor", "middle")
      .text(variable);
  }
  
  // Initialize with precipitation histogram
  drawHistogram(data, "precipitation");

  // Create drop-down menu
  var dropdown = d3
    .select("body")
    .append("select")
    .attr("id", "variable-select")
    .on("change", function() {
      var variable = d3.select(this).property("value");
      drawHistogram(data, variable);
    });

    // Add options to drop-down menu
dropdown
    .append("option")
    .text("Precipitation")
    .attr("value", "precipitation");
    
  dropdown
    .append("option")
    .text("Max Temperature")
    .attr("value", "temp_max");
  dropdown
    .append("option")
    .text("Min Temperature")
    .attr("value", "temp_min");
  dropdown
    .append("option")
    .text("Wind")
    .attr("value", "wind");

  // Create x-axis group
  svg
    .append("g")
    .attr("class", "x-axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Create y-axis group
  svg
    .append("g")
    .attr("class", "y-axis")
    .call(yAxis);
});

