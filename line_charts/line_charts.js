var people = ["Arno", "Curt", "Jon"]
var wrists = ["left", "right"]
for (i = 0; i < people.length; i++) {
  for (j = 0; j < wrists.length; j++) {
    d3.select("charts")
      .append("svg")
      .attr("person", people[i])
      .attr("wrist", wrists[j])
      .attr("width", 960)
      .attr("height", 500);
  }
}