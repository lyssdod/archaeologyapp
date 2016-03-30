//Geolocation
function initMap() {
  var myCenter=new google.maps.LatLng(50.4501,30.5234);
  var mapProp = {
center:myCenter,
       zoom:5,
       mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map"),mapProp)

    var geocoder = new google.maps.Geocoder();
  var infowindow = new google.maps.InfoWindow;

  document.getElementById('submit').addEventListener('click', function() {
      geocodeAddress(geocoder, map);
      });

  google.maps.event.addListener(map, 'click', function(event) {
      geocodeLatLng(geocoder, map, infowindow, event.latLng);
      });

  document.getElementById('reset').addEventListener('click', function() {

      var myCenter=new google.maps.LatLng(50.4501,30.5234);
      var mapProp = {
center:myCenter,
zoom:5,
mapTypeId:google.maps.MapTypeId.ROADMAP
};
map = new google.maps.Map(document.getElementById("map"),mapProp)

var geocoder = new google.maps.Geocoder();

document.getElementById('submit').addEventListener('click', function() {
  geocodeAddress(geocoder, map);
  });
google.maps.event.addListener(map, 'click', function(event) {
      geocodeLatLng(geocoder, map, infowindow, event.latLng);
      });
});

}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
map: resultsMap,
position: results[0].geometry.location
});
      } else {
      alert('Geocode was not successful for the following reason: ' + status);
      }
      });
}

function geocodeLatLng(geocoder, map, infowindow, location) {

  var latlng = {lat: location.lat(), lng: location.lng()};
  geocoder.geocode({'location': latlng}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
      if (results[1]) {
      map.setZoom(9);
      var marker = new google.maps.Marker({
position: latlng,
map: map
});
      infowindow.setContent(results[1].formatted_address + "<br>" +location.lat() +"<br>"+ location.lng());
      infowindow.open(map, marker);
      var oblast = document.getElementById('oblast').value=results[1].formatted_address;
      var rajon = document.getElementById('rajon').value=results[1].formatted_address;
      var krajina = document.getElementById('krajina').value=results[1].formatted_address;
      } else {
      window.alert('No results found');
      }
      } else {
      window.alert('Geocoder failed due to: ' + status);
      }
      });
}

