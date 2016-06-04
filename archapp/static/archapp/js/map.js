// working with the map

(function(obj)
{
    // will be called by google api
    obj.init = function()
    {
        var dlat = 50.2700; 
        var dlon = 30.3124;
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

        obj.pos = { lat: clat, lng: clon };
        obj.handle = new google.maps.Map(document.getElementById('map'), 
        {
            zoom: zoom,
            center: obj.pos,
            mapTypeId: google.maps.MapTypeId.ROADMAP
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

    // save marker data back to the input fields
    obj.storeData = function()
    {
        var loc = obj.marker.getPosition();

        document.getElementById('id_latitude').value = loc.lat();
        document.getElementById('id_longtitude').value = loc.lng();

        obj.elevator.getElevationForLocations({ 'locations': [loc] }, function(results, status)
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

        google.maps.event.addListener(obj.handle, 'click', function(event)
        {
            obj.marker.setPosition(event.latLng);
            obj.storeData();
        });
        google.maps.event.addListener(obj.marker, 'dragend', function(event)
        {
            obj.storeData();
        });
    }


})(archapp.Map);

function initmap()
{
    archapp.Map.init();
}
