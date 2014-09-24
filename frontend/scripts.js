var map = L.map('map').setView([33.4150, -111.8314], 13);

L.tileLayer('http://{s}.tiles.mapbox.com/v3/ardouglass.h3mingmm/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

function geocodeText(text) {
  console.log(text);
   $.ajax({
    type: 'POST',
    crossDomain: true,
    url: 'http://findlines.herokuapp.com/',
    data: { fileupload: text},
    dataType: 'json',
    success: populateMap
  });
};

function populateMap(line) {
  var districtLines = L.geoJson().addTo(map);
  lines = line.text;
  $.each(lines, function(line) {
    console.log("mapping: " + line[0]);
    districtLines.addData($.parseJSON(line[1]));
  });
}

$(function() {
  $("#geocode").on("click", geocodeText($("#geotext").value));
});
