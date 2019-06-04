function init() {
  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
  window.URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
  video = document.querySelector('video');
  //debug("Please, grant access to the camera!");
  if (navigator.getUserMedia) {
    navigator.getUserMedia({video: true}, 
      function(stream) {
       if (video.mozSrcObject !== undefined) {
          video.mozSrcObject = stream;
        } else {
          video.srcObject = stream;
        }
        video.play();  
        debug("Webcam on!");
      }, 
      function() {
        //debug("No webcam or access denied");
        window.alert("dwada");
      }
    );     
  } else {
    //debug('getUserMedia not supported!');
    window.alert("wdwad");
  }
}

function debug(s) {
  document.querySelector("#debug").innerHTML = s;
}