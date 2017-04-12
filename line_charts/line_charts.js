// define datasets
var people = ["Arno", "Curt", "Jon"]
var wrists = ["left", "right"]
var axes = ['x', 'y', 'z']

// build canvases
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
    }
  }
}

// build graphs
for (i = 0; i < people.length; i++) {
  for (j = 0; j < wrists.length; j++) {
    for (k = 0; k < axes.length; k++) {
        var svg = d3.select("charts").select("svg[person=" + people[i] +
                   "][wrist=" + wrists[j] + "][axis=" + axes[k] + "]"),
          margin = {top: 5, right: 80, bottom: 5, left: 50},
          width = svg.attr("width") - margin.left - margin.right,
          height = svg.attr("height") - margin.top - margin.bottom,
          g = svg.append("g").attr("transform", "translate(" + margin.left +
              "," + margin.top + ")");
     g.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2) + 26)
        .attr("text-anchor", "middle")
        .text(people[i] + ", " + wrists[j] + " wrist, " + axes[k] + " axis");
      
     switch(i) {
       case 0:
         switch(j) {
           case 1:
             var data = d3.csv(
                        'https://osf.io/gse6b/?action=download&version=1');
           default:
             var data = '';
         }
        default:
          var data = '';
     }
      
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