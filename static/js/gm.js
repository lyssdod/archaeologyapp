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
      map.setCenter(results[1].geometry.location);
      map.setZoom(9);
      var marker = new google.maps.Marker({
position: latlng,
map: map
});
      infowindow.setContent(results[1].formatted_address + "<br>" +location.lat() +"<br>"+ location.lng());
      infowindow.open(map, marker);
      var x;
      var rajon;
      for (x in results[0].address_components) {
        if (results[0].address_components[x].types[0] == "administrative_area_level_2") {

          rajon = results[0].address_components[x].long_name;
        }
      }
      if (rajon == undefined){
        for (x in results[0].address_components) {
          if (results[0].address_components[x].types[0] == "administrative_area_level_3") {
            rajon = results[0].address_components[x].long_name;
          }
        }
      }

document.getElementById('rajon').value= rajon;
var x;
var oblast;
for (x in results[0].address_components) {
  if (results[0].address_components[x].types[0] == "administrative_area_level_1") {

    oblast = results[0].address_components[x].long_name;
  } 
} 
document.getElementById('oblast').value= oblast;

var obj = JSON.stringify(results[0].address_components[3])
  document.getElementById('obj').innerHTML = obj;
  } else {
    window.alert('No results found');
  }
} else {
  window.alert('Geocoder failed due to: ' + status);
}
});
}

