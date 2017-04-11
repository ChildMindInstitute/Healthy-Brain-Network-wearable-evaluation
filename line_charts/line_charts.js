var people = ["Arno", "Curt", "Jon"]
var wrists = ["left", "right"]
var axes = ['x', 'y', 'z']
for (i = 0; i < people.length; i++) {
  for (j = 0; j < wrists.length; j++) {
    for (k = 0; k < axes.length; k++) {
      d3.select("charts")
        .append("svg")
        .attr("person", people[i])
        .attr("wrist", wrists[j])
        .attr("axis", axes[k])
        .attr("width", 960)
        .attr("height", 500);
      
      var svg = d3.select("svg"),
          margin = {top: 20, right: 80, bottom: 30, left: 50},
          width = svg.attr("width") - margin.left - margin.right,
          height = svg.attr("height") - margin.top - margin.bottom,
          g = svg.append("g").attr("transform", "translate(" + margin.left +
              "," + margin.top + ")");
            
      var parseTime = d3.timeParse("%m-%d %H:%M:%S.$L");
    
      var x = d3.scaleTime().range([0, width]),
          y = d3.scaleLinear().range([height, 0]),
          z = d3.scaleOrdinal(d3.schemeCategory10);
        
      var line = d3.line()
                   .curve(d3.curveBasis)
                   .x(function(d) { return x(d.date); })
                   .y(function(d) { return y(d.temperature); });
    }
  }
}