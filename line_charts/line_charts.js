// define datasets
var people = ["Arno", "Curt", "Jon"];
var wrists = ["left", "right"];
var axes = ['x', 'y', 'z'];
var devices = [
  "Actigraph",
  "E4",
  "Embrace",
  "GENEActiv_black",
  "GENEActiv_pink",
  "Wavelet"
];


// build canvases
for (i = 0; i < people.length; i += 1) {
  for (j = 0; j < wrists.length; j += 1) {
    for (k = 0; k < axes.length; k += 1) {
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
for (i = 0; i < people.length; i += 1) {
  for (j = 0; j < wrists.length; j += 1) {
    for (k = 0; k < axes.length; k += 1) {
        var svg = d3.select("charts").select("svg[person=" + people[i] +
                   "][wrist=" + wrists[j] + "][axis=" + axes[k] + "]");
        var margin = {top: 5, right: 80, bottom: 5, left: 50};
        var width = svg.attr("width") - margin.left - margin.right;
        var height = svg.attr("height") - margin.top - margin.bottom;
        var g = svg.append("g").attr("transform", "translate(" + margin.left +
              "," + margin.top + ")");
        g.append("text")
         .attr("x", (width / 2))             
         .attr("y", 0 - (margin.top / 2) + 26)
         .attr("text-anchor", "middle")
         .text(people[i] + ", " + wrists[j] + " wrist, " + axes[k] + " axis");
      for (l = 0; l < devices.length; l += 1) {
         d3.csv("../organized/accelerometer/" + people[i] + "_" +
                wrists[j] + "_" + devices[l] + ".csv", function(data, error) {
                  if(error){throw error;}
                  console.log(data)
                });
      }
    }
  }
}