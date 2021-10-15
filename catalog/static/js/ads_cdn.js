  //fetching user ip address
  function trackIP() {
    var trackurl = 'http://localhost:8000/catalog/api/track-ip/';
    fetch(trackurl)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
  }
  
  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(getPosition);
    } else {
      console.log("Geolocation is not supported by this browser");
    }
  }
  
  function getPosition(position) {
    console.log("Latitude: " + position.coords.latitude + 
    ", Longitude: " + position.coords.longitude);
  }
  
  //fetching user ip address
  function trackCookies() {
    var trackurl = 'http://localhost:8000/catalog/api/track-cookies/';
    fetch(trackurl)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
  }
  
  document.getElementById('ads_section').addEventListener('click', trackIP);
  