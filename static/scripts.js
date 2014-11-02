var lg = {};

// mesa latlong = [33.4150, -111.8314]
// nyc = [40.7210,-73.9823]
var localized_latlong = [40.7210,-73.9823];

var placename = "nyc";

var map = L.map('map').setView(localized_latlong, 11);
L.tileLayer('http://{s}.tiles.mapbox.com/v3/ardouglass.h3mingmm/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

function geocodeText(text, placename) {
   $.ajax({
    type: 'POST',
    url: '/', // set URL to http://www.streetsear.ch/ if you want to test against the server
    data: { sentence: text, placename: placename},
    dataType: 'json',
    success: populateMap
  });
}

function populateMap(response) {
  // add a new layer to the map
  lg.features = L.geoJson(null, {
    style: { color: '#0a1e0a', weight: 5 },
    onEachFeature: function (feature, layer) {

      var el = $("<div>"+feature.properties.founditem+"</div>");
      $("#found-roads").append(el);
      if (layer instanceof L.Marker){
        layer.setOpacity(0.5);
      }

      // Show which found item is being hovered over
      el.hover(function() {
        if (layer instanceof L.Marker){
          layer.setOpacity(1);
        } else { // assume we're dealing with a line
          layer.setStyle( { color: '#329632', weight: 7 } );
        }
        $(this).css('font-weight', 'bold');
        $(this).css('color', '#329632');
      }, function() {
        if (layer instanceof L.Marker){
          layer.setOpacity(0.5);
        } else { // assume we're dealing with a line
          layer.setStyle( { color: '#0a1e0a', weight: 5 } );
        }
        $(this).css('font-weight', 'normal');
        $(this).css('color', 'black');
      });
    }
  }).addTo(map);

  features = response.text;
  _.forEach(features, function(feature) {

    // Add to map
    var data = $.parseJSON(feature[1]);
    data.properties = { 'founditem': feature[0] };
    lg.features.addData(data);
  });

  // No data, no button
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

    // clear any old results.
    $("#found-roads").empty();

    // send off the text for geocoding
    geocodeText($("#geotext").val(),placename);

    // Let users know something is happening
    $("#geocode").text("Hold up. Processing.").css("background-color", "#ef1818");
  });

  // Quick and Hacky Tabs
  $(".tabs").click(function(e) {
    e.preventDefault();

    var target = $(e.target);
    var clickedTab = target.data("tab");

    if (clickedTab == "input") {
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
    $('.tabs .pure-menu-selected').removeClass('pure-menu-selected');
    target.parent("li").toggleClass('pure-menu-selected');
  });

  $(".cities").click(function(e) {
    e.preventDefault();

    var target = $(e.target);
    var clickedTab = target.data("tab");

    if (clickedTab == "chicago") {
      map.panTo(new L.LatLng(41.8376, -87.6818)); //dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "chicago";
    }
    else if (clickedTab == "dc") {
      map.panTo(new L.LatLng(38.9041, -77.0171)); //dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "dc";
    }
    else if (clickedTab == "nyc") {
      map.panTo(new L.LatLng(40.7283, -73.9942)); //dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "nyc";
    }
    else if (clickedTab == "sf") {
      map.panTo(new L.LatLng(37.7599, -122.437)); //dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "sf";
    }
    else if (clickedTab == "portland") {
      map.panTo(new L.LatLng(45.537, -122.65)); //portland GeoPosition[{45.537, -122.65}] dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "portland";
    }
    else if (clickedTab == "dallas") {
      map.panTo(new L.LatLng(32.7942, -96.7655)); //dallas: GeoPosition[{32.7942, -96.7655}] portland GeoPosition[{45.537, -122.65}] dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "dallas";
    }
    else if (clickedTab == "mesa") {
      map.panTo(new L.LatLng(33.4019, -111.717)); //mesa GeoPosition[{}], dallas: GeoPosition[{32.7942, -96.7655}] portland GeoPosition[{45.537, -122.65}] dc GeoPosition[{38.9041, -77.0171}] nyc GeoPosition[{40.7283, -73.9942}] sf GeoPosition[{37.7599, -122.437}]
      placename = "mesa";
    }
    // Only show active tab
    $('.cities .pure-menu-selected').removeClass('pure-menu-selected');
    target.parent("li").toggleClass('pure-menu-selected');
  });

  // Export as GeoJSON
  $("#export").click(function(e) {
    e.preventDefault();

    $("#geojson").val(JSON.stringify(lg.features.toGeoJSON()));

    $("#map").toggle();
    $("#geojson").toggle();
  });

});
