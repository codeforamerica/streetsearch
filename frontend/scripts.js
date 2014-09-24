var lg = {};

var map = L.map('map').setView([33.4150, -111.8314], 11);
L.tileLayer('http://{s}.tiles.mapbox.com/v3/ardouglass.h3mingmm/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

function geocodeText(text) {
   $.ajax({
    type: 'POST',
    crossDomain: true,
    url: 'http://findlines.herokuapp.com',
    data: { fileupload: text},
    dataType: 'json',
    success: populateMap
  });
};

function populateMap(line) {
  console.log(line);
  lg.districtLines = L.geoJson().addTo(map);
  lines = line.text;
  _.forEach(lines, function(line) {
    
    // Add to found list
    $("#found-roads").append("<p>" + line[0] + "</p>");
    
    // Add to map
    lg.districtLines.addData($.parseJSON(line[1]));
  });

  $("#export").show();

  // Force show the "Found" tab
  $("a[data-tab='found']").click();

  // Reset state of button
  $("#geocode").text("Geocode This Text").css("background-color", "#329632");
}

// Event Handlers
$(function() {

  // Geocode
  $("#geocode").click(function(e) {
    e.preventDefault();
    geocodeText($("#geotext").val());

    // Let users know something is happening
    $("#geocode").text("Hold up. Processing.").css("background-color", "#ef1818");
  });

  // Quick and Hacky Tabs
  $(".tabs").click(function(e) {
    e.preventDefault();

    var target = $(e.target);
    var clickedTab = target.data("tab");

    if(clickedTab == "input") {
      $(".input.panel").show();
      $(".found.panel").hide();
      //$(".wtf.panel").hide();
    } 
    else if (clickedTab == "found") {
      $(".input.panel").hide();
      $(".found.panel").show();
      //$(".wtf.panel").hide();
    }
    else if (clickedTab == "wtf") {
      $(".input.panel").hide();
      $(".found.panel").hide();
     //$(".wtf.panel").show();      
    }

    // Only show active tab
    $('.pure-menu-selected').removeClass('pure-menu-selected');
    target.parent("li").toggleClass('pure-menu-selected');
  });

  // Export as GeoJSON
  $("#export").click(function(e) {
    e.preventDefault();

    $("#geojson").val(JSON.stringify(lg.districtLines.toGeoJSON()));

    $("#map").toggle();
    $("#geojson").toggle();
  });

});
