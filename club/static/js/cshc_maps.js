
// Load the Google Maps script. 
// IMPORTANT: When done, this will call the 'callback' function.
function loadScript(callback) {
    var script = document.createElement("script");
    script.type = "text/javascript";
    // This Google Maps API key is associated with the CSHC Google APIs project: https://code.google.com/apis/console/?pli=1#project:533261630005:access
    // This account was set up by mcculloch.graham@gmail.com
    script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDdK_W-7S1O_tiuK2sr5O8oUlTnXReouVU&sensor=false&callback=" + callback;
    document.body.appendChild(script);
}