//Geolocation
// 
// track markers
var markers = [];
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function clearMarkers() {
  setMapOnAll(null);
}

//Geocoding
function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
          position: results[0].geometry.location
      });
      markers.push(marker);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
//Reverse Geocoding
function geocodeLatLng(geocoder, map, infowindow, location) {

  var latlng = {lat: location.lat(), lng: location.lng()};
  geocoder.geocode({'location': latlng}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      if (results[1]) {
        map.setCenter(results[1].geometry.location);
        var marker = new google.maps.Marker({
          position: latlng,
            map: map
        });
        markers.push(marker);
        var lat = String(location.lat());
        var lng = String(location.lng());
        infowindow.setContent(results[1].formatted_address + "<br>" + lat.slice(0,6) +", "+ lng.slice(0,6));
        infowindow.open(map, marker);
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

        document.getElementById('id_district').value= rajon;
        var oblast;
        for (x in results[0].address_components) {
          if (results[0].address_components[x].types[0] == "administrative_area_level_1") {

            oblast = results[0].address_components[x].long_name;
          } 
        } 
        document.getElementById('id_region').value= oblast;
        var krajina;
        for (x in results[0].address_components) {
          if (results[0].address_components[x].types[0] == "country") {

            krajina = results[0].address_components[x].long_name;
          } 
        } 
        document.getElementById('id_country').value= krajina;
        var latd;
        latd = location.lat();
        document.getElementById('id_latitude').value= latd;
        var longt;
        longt = location.lng();
        document.getElementById('id_longtitude').value= longt;



        //var obj = JSON.stringify(results[0].address_components[3]);
        //document.getElementById('obj').innerHTML = obj;
      } else {
        window.alert('No results found');
      }
    } else {
      window.alert('Geocoder failed due to: ' + status);
    }
  });
}


