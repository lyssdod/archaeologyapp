// Init the Map
function initMap() {
  var defaultLat = 50.2700; 
  var defaultLong = 30.3124;
  var defaultCenter=new google.maps.LatLng(defaultLat, defaultLong);

  var mapProp = {
    center:defaultCenter,
    zoom:5,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map"),mapProp);

  var geocoder = new google.maps.Geocoder();
  var infowindow = new google.maps.InfoWindow;
  var elevator = new google.maps.ElevationService;
  document.getElementById('submit').addEventListener('click', function() {
    clearMarkers();
    geocodeAddress(geocoder, map);
  });

  google.maps.event.addListener(map, 'click', function(event) {
    clearMarkers();
    geocodeLatLng(geocoder, map, infowindow, event.latLng);
   console.log( displayLocationElevation(event.latLng, elevator)
     ); 
  });

  document.getElementById('reset').addEventListener('click', initMap);

}

