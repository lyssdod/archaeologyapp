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

        obj.pos = { lat: clat, lng: clon };
        obj.handle = new google.maps.Map(document.getElementById('map'), 
        {
            zoom: zoom,
            center: obj.pos,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        if(obj.siteview)
            obj.marker = new google.maps.Marker({
                position: obj.pos,
                map: obj.handle
            });
        else
        {
            obj.marker = false;
            obj.setupHandler();
        }
    }

    // save marker position back to the input fields
    obj.storePosition = function()
    {
        var loc = obj.marker.getPosition();

        document.getElementById('id_latitude').value = loc.lat();
        document.getElementById('id_longtitude').value = loc.lng();
    }

    // handle location picking
    obj.setupHandler = function()
    {
        google.maps.event.addListener(obj.handle, 'click', function(event)
        {
            var picked = event.latLng;

            // create the marker
            if(obj.marker === false)
            {
                obj.marker = new google.maps.Marker({
                    position: picked,
                    map: obj.handle,
                    draggable: true
                });

                // listen for drag events
                google.maps.event.addListener(obj.marker, 'dragend', function(event) {
                    obj.storePosition();
                });
            }
            else
                obj.marker.setPosition(picked);

            // ...and now we need to
            obj.storePosition();
        });
    }

})(archapp.Map);

function initmap()
{
    archapp.Map.init();
}
