// working with the map

(function(obj)
 {
   // will be called by google api
   obj.init = function()
{
  var dlat = parseFloat(document.getElementById('id_latitude').value);
  var dlon = parseFloat(document.getElementById('id_longtitude').value);
  var dmap = document.getElementById('map');
  if(dmap)
{
  if (!dlat) {
    var dlat = 51.528397002221;
    var dlon = 30.625762939453;
  };
  var clat = 0.00;
  var clon = 0.00;
  var zoom = 5;
  var parm = {};

  if(obj.siteview)
{
  zoom = 7;
  clat = parseFloat(document.getElementById('lat').value);
  clon = parseFloat(document.getElementById('lon').value);

  // failed to parse stored data
  if(isNaN(clat) || isNaN(clon))
  {
    clat = dlat;
    clon = dlon;
    zoom = 5;
  }
}
else
{
  clat = dlat;
  clon = dlon;
}

obj.pos = new google.maps.LatLng(clat, clon);
obj.handle = new google.maps.Map(dmap,
    {
      zoom: zoom,
  center: obj.pos,
  mapTypeId: google.maps.MapTypeId.TERRAIN
    });

// setup marker default params
parm.position = obj.pos;
parm.map   = obj.handle;

if( !obj.siteview )
  parm.draggable = true;

  // create marker
  obj.marker = new google.maps.Marker(parm);

  // create handlers and fill fields with data for obj.pos
if( !obj.siteview )
{
  obj.setupHandlers();
  obj.storeData();
}
}
}

// save marker data back to the input fields
obj.storeData = function()
{
  document.getElementById('id_latitude').value = obj.pos.lat();
  document.getElementById('id_longtitude').value = obj.pos.lng();

  obj.geocoder.geocode({ 'location': obj.pos }, function(results, status)
      {
        if (status === google.maps.GeocoderStatus.OK)
  {
    if (results[0])
  {
    document.getElementById('id_country').value = obj.getSubset(results[0], ['country']);
    document.getElementById('id_region').value = obj.getSubset(results[0], ['administrative_area_level_1']);
    document.getElementById('id_district').value = obj.getSubset(results[0], ['administrative_area_level_2', 'administrative_area_level_3']);
    document.getElementById('id_settlement').value = obj.getSubset(results[0], ['locality', 'route']);
  }
    else
    window.alert('No results found');
  }
        else
    window.alert('Geocoder failed due to: ' + status);
      });
  obj.elevator.getElevationForLocations({ 'locations': [obj.pos] }, function(results, status)
      {
        if (status === google.maps.ElevationStatus.OK)
  {
    var elv = 0;

    if (results[0])
    elv = results[0].elevation;

  document.getElementById('id_altitude').value = Math.round(elv);
  }
        else
    alert('Elevation service failed due to: ' + status);
      });


}

// handle location picking and dragging
obj.setupHandlers = function()
{
  obj.elevator = new google.maps.ElevationService;
  obj.geocoder = new google.maps.Geocoder;

  google.maps.event.addListener(obj.handle, 'click', function(event)
      {
        obj.pos = event.latLng;
        obj.marker.setPosition(obj.pos);
        obj.storeData();
      });
  google.maps.event.addListener(obj.marker, 'dragend', function(event)
      {
        obj.pos = event.latLng;
        obj.storeData();
      });
}

// get needed addr subset
obj.getSubset = function(address, subset)
{
  for (i = address.address_components.length; i--;)
    if (subset.indexOf(address.address_components[i].types[0]) >= 0)
      return address.address_components[i].long_name;
}

})(archapp.map);

function initmap()
{
  archapp.map.init();
}
