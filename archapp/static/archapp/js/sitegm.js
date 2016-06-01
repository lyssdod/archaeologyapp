//Site Map
function initMap() {
  var defaultLat = 50.2700; 
  var defaultLong = 30.3124;
  var siteLat;
  var siteLong;
  siteLat = document.getElementById("Lat").value;
  siteLong = document.getElementById("Lng").value;
  console.log(siteLat)
    if (siteLat) {
      var defaultCenter=new google.maps.LatLng(siteLat, siteLong);
      var zm = 7;
    } else {
      var defaultCenter=new google.maps.LatLng(defaultLat, defaultLong);
      var zm = 5;
    }
  var mapProp = {
    center:defaultCenter,
    zoom:zm,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map2"),mapProp);
  var siteposition=new google.maps.LatLng(siteLat, siteLong);
  var geocoder = new google.maps.Geocoder();
  var infowindow = new google.maps.InfoWindow;
  if (siteLat) {
    geocodeLatLng(geocoder, map, infowindow, siteposition);
  };
}

