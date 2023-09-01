let input1 = document.getElementById('from');
let input2 = document.getElementById('to');
const form = document.querySelector('form');
form.addEventListener('submit', calcRoute)

// gives autocomplete function to inputs
let autocomplete1 = new google.maps.places.Autocomplete(input1);
let autocomplete2 = new google.maps.places.Autocomplete(input2);

let myLatLng = {
    lat: 37.839333,
    lng: -84.270020
};

let mapOptions = {
    center: myLatLng,
    zoom: 7,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

let map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);

var directionsService = new google.maps.DirectionsService();

var directionsDisplay = new google.maps.DirectionsRenderer();

directionsDisplay.setMap(map);

function calcRoute(e){
    e.preventDefault();
    let request = {
        origin:document.getElementById('from').value,
        destination:document.getElementById('to').value,
        travelMode:google.maps.TravelMode.DRIVING,
        unitSystem:google.maps.UnitSystem.IMPERIAL
    }
    console.log(request);
    directionsService.route(request, function(result, status){
        if(status == google.maps.DirectionsStatus.OK){
            const output = document.querySelector('#output');
            output.innerHTML = 
                "<div class='alert-info'>From: " +
                document.getElementById('from').value +
                ".<br />To: " +
                document.getElementById('to').value +
                ".<br /> Driving distance <i class='fas fa-road'></i> : " +
                result.routes[0].legs[0].distance.text +
                ".<br />Duration <i class='fas fa-hourglass-start'></i> : " +
                result.routes[0].legs[0].duration.text +
                ".</div>";
            
            directionsDisplay.setDirections(result)
        }
        else {
            directionsDisplay.setDirections({ routes: [] });
            map.setCenter(myLatLng);
            output.innerHTML = 
            "<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve directions</div>"
        }
    })
};


function prevent(e){
    e.preventDefault();
}