var gmap = {
     options: null,
     map: null,
     marker: null,
     init: function (elem, opts) {
         this.options = opts;
         this.map = new google.maps.Map(document.getElementById(elem), this.options);
         google.maps.event.trigger(this.map, 'resize');
     },
     setMarkerPosition: function (latLng) {
         if (this.marker == null) this.marker = this.createMarker();
         this.marker.setPosition(latLng);
         this.modifyInputs(this.marker.getPosition());
         this.map.setCenter(latLng);
     },
     createMarker: function () {
         return new google.maps.Marker({
             map: this.map
         });
     },
     modifyInputs: function (locData) {
         $('input#id_lat').val(locData.lat());
         $('input#id_lon').val(locData.lng());
     },
     initEvents: function () {
         var self = this;
         google.maps.event.addListener(this.map, 'click', function (e) {
             self.setMarkerPosition(e.latLng);
         });
     }
 };
window.map_loaded = false;
 $(document).ready(function () {
     var contact_info_tab_id = 'for_tabs-6';
     $('a#'+contact_info_tab_id).click(function(){
         if (!window.map_loaded)$.getScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyBiEZSlPQieF-33H0ivYHVTQNVlvAlHF6c&sensor=true&language=tr&callback=show_map');
     });
 });

function show_map(){
    window.map_loaded = true;
     var lat = $('input#id_lat');
     var lon = $('input#id_lon');
     lat.parent().css('display', 'none');
     lon.parent().css('display', 'none');
     if (lat.length && lon.length) {
         lon.parent().after('<div id="gmap"></div>');
         var markerAvailable = false;
         var lat_value = parseFloat(lat.val());
         var lon_value = parseFloat(lon.val());
         if (lat_value == '0.0' && lon_value == '0.0') {
             lat_value = parseFloat('38.463556');
             lon_value = parseFloat('26.888075');
         } else markerAvailable = true;

         var mapOptions = {
             center: new google.maps.LatLng(lat_value, lon_value),
             zoom: 12,
             mapTypeId: google.maps.MapTypeId.ROADMAP
         };
         gmap.init('gmap', mapOptions);
         gmap.initEvents();
         if (markerAvailable) {
             var latLngObj = new google.maps.LatLng(lat_value, lon_value);
             gmap.setMarkerPosition(latLngObj);
         }

         // geolocation ile haritayi kullanicinin bulundugu bolgede acma
         if (navigator.geolocation) {
             navigator.geolocation.getCurrentPosition(function (e) {
                 var geoLat = e.coords.latitude;
                 var geoLon = e.coords.longitude;
                 gmap.map.setCenter(new google.maps.LatLng(geoLat, geoLon));
                 $('input#id_lat').val(geoLat);
                 $('input#id_lon').val(geoLon);
             }, function (error) {

             });
         }
         parent.mainframe.load();

     }
 }
