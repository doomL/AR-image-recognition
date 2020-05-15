/*

>> kasperkamperman.com - 2018-04-18
>> https://www.kasperkamperman.com/blog/camera-template/

*/

var takeSnapshotUI = createClickFeedbackUI();
var video;
var takePhotoButton;
var toggleFullScreenButton;
var switchCameraButton;
var amountOfCameras = 0;
var currentFacingMode = 'environment';

var snap = 0;
var recorder;

$(document).ready(function() {
    let namespace = "/test";
    let video = document.querySelector("#videoElement");
    console.log(video);
    let canvas = document.querySelector("#canvasElement");
    let ctx = canvas.getContext('2d');

    var localMediaStream = null;

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);



    // socket.on('connect', function() {
    //     console.log('Connected!');

    // });
    socket.on('connection', (socketServer) => {
        console.log("connected")
    });
    
    
    
    socket.on('responseImageInfo', function(imageRecognized) {
        var json = JSON.parse(imageRecognized);

              
        iziToast.show({
            id: 'recog',
            theme: 'dark',
            icon: 'icon-contacts',
            title: json.name,
            displayMode: 2,
            message: 'Ho riconosciuto questa immagine </br>'+ json.model+ json.type,
            position: 'topCenter',
            transitionIn: 'flipInX',
            transitionOut: 'flipOutX',
            progressBarColor: 'rgb(0, 255, 184)',
            image: json.base64,
            imageWidth: 70,
            layout: 2,
            onClosing: function(){
                console.info('onClosing');
            },
            onClosed: function(instance, toast, closedBy){
                console.info('Closed | closedBy: ' + closedBy);
            },
            iconColor: 'rgb(0, 255, 184)'
        });
        
    });

    








    var constraints = {
        video: {
            width: { min: 640 },
            height: { min: 480 }
        }
    };

    // socket.on('message', function(mess) {
    //     alert(mess)
    //     console.log("PROVA STAPA", mess)
    // });
    setInterval(function() {
        sendSnapshot();

    }, 1000);
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        video.srcObject = stream;
        localMediaStream = stream;

    }).catch(function(error) {
        console.log(error);
    });

    function sendSnapshot() {


        if (!localMediaStream) {
            return;
        }
        console.log("invioooooo")
        canvas.height = 480
        canvas.width = 854
        ctx.drawImage(video, 0, 0, 854, 480);
        //ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 1920, 1080);

        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('input image', dataURL);
    }
});

document.addEventListener("DOMContentLoaded", function(event) {

    // do some WebRTC checks before creating the interface
    DetectRTC.load(function() {

        // do some checks
        if (DetectRTC.isWebRTCSupported == false) {
            alert('Please use Chrome, Firefox, iOS 11, Android 5 or higher, Safari 11 or higher');
        } else {
            if (DetectRTC.hasWebcam == false) {
                alert('Please install an external webcam device.');
            } else {

                amountOfCameras = DetectRTC.videoInputDevices.length;

                initCameraUI();
                //initCameraStream();
            }
        }

        console.log("RTC Debug info: " +
            "\n OS:                   " + DetectRTC.osName + " " + DetectRTC.osVersion +
            "\n browser:              " + DetectRTC.browser.fullVersion + " " + DetectRTC.browser.name +
            "\n is Mobile Device:     " + DetectRTC.isMobileDevice +
            "\n has webcam:           " + DetectRTC.hasWebcam +
            "\n has permission:       " + DetectRTC.isWebsiteHasWebcamPermission +
            "\n getUserMedia Support: " + DetectRTC.isGetUserMediaSupported +
            "\n isWebRTC Supported:   " + DetectRTC.isWebRTCSupported +
            "\n WebAudio Supported:   " + DetectRTC.isAudioContextSupported +
            "\n is Mobile Device:     " + DetectRTC.isMobileDevice
        );

    });

});

function initCameraUI() {

    video = document.getElementById('videoElement');

    takePhotoButton = document.getElementById('takePhotoButton');
    toggleFullScreenButton = document.getElementById('toggleFullScreenButton');
    switchCameraButton = document.getElementById('switchCameraButton');
    backButton = document.getElementById('backButton');

    // https://developer.mozilla.org/nl/docs/Web/HTML/Element/button
    // https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Techniques/Using_the_button_role

    takePhotoButton.addEventListener("click", function() {
        takeSnapshotUI();
        takeSnapshot();
    });

    backButton.addEventListener("click", function() {
        window.location.replace("/");
    });
    // -- fullscreen part

    function fullScreenChange() {
        if (screenfull.isFullscreen) {
            toggleFullScreenButton.setAttribute("aria-pressed", true);
        } else {
            toggleFullScreenButton.setAttribute("aria-pressed", false);
        }
    }

    if (screenfull.enabled) {
        screenfull.on('change', fullScreenChange);

        toggleFullScreenButton.style.display = 'block';

        // set init values
        fullScreenChange();

        toggleFullScreenButton.addEventListener("click", function() {
            screenfull.toggle(document.getElementById('container')).then(function() {
                console.log('Fullscreen mode: ' + (screenfull.isFullscreen ? 'enabled' : 'disabled'))
            });
        });
    } else {
        console.log("iOS doesn't support fullscreen (yet)");
    }

    // -- switch camera part
    if (amountOfCameras > 1) {

        switchCameraButton.style.display = 'block';

        switchCameraButton.addEventListener("click", function() {

            if (currentFacingMode === 'environment') currentFacingMode = 'user';
            else currentFacingMode = 'environment';

            initCameraStream();

        });
    }

    // Listen for orientation changes to make sure buttons stay at the side of the 
    // physical (and virtual) buttons (opposite of camera) most of the layout change is done by CSS media queries
    // https://www.sitepoint.com/introducing-screen-orientation-api/
    // https://developer.mozilla.org/en-US/docs/Web/API/Screen/orientation
    window.addEventListener("orientationchange", function() {

        // iOS doesn't have screen.orientation, so fallback to window.orientation.
        // screen.orientation will 
        if (screen.orientation) angle = screen.orientation.angle;
        else angle = window.orientation;

        var guiControls = document.getElementById("gui_controls").classList;
        var vidContainer = document.getElementById("vid_container").classList;

        if (angle == 270 || angle == -90) {
            guiControls.add('left');
            vidContainer.add('left');
        } else {
            if (guiControls.contains('left')) guiControls.remove('left');
            if (vidContainer.contains('left')) vidContainer.remove('left');
        }

        //0   portrait-primary   
        //180 portrait-secondary device is down under
        //90  landscape-primary  buttons at the right
        //270 landscape-secondary buttons at the left
    }, false);

}

// https://github.com/webrtc/samples/blob/gh-pages/src/content/devices/input-output/js/main.js
// function initCameraStream() {

//     // stop any active streams in the window
//     if (window.stream) {
//         window.stream.getTracks().forEach(function(track) {
//             track.stop();
//         });
//     }

//     var constraints = {
//         audio: false,
//         video: {
//             //width: { min: 1024, ideal: window.innerWidth, max: 1920 },
//             //height: { min: 776, ideal: window.innerHeight, max: 1080 },
//             facingMode: currentFacingMode
//         }
//     };

//     navigator.mediaDevices.getUserMedia(constraints).
//     then(handleSuccess).catch(handleError);

//     function handleSuccess(stream) {

//         window.stream = stream; // make stream available to browser console
//         video.srcObject = stream;

//         if (constraints.video.facingMode) {

//             if (constraints.video.facingMode === 'environment') {
//                 switchCameraButton.setAttribute("aria-pressed", true);
//             } else {
//                 switchCameraButton.setAttribute("aria-pressed", false);
//             }
//         }

//         return navigator.mediaDevices.enumerateDevices();
//     }

//     function handleError(error) {

//         console.log(error);

//         //https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
//         if (error === 'PermissionDeniedError') {
//             alert("Permission denied. Please refresh and give permission.");
//         }

//     }

// }

function takeSnapshot() {

    console.log(snap + " snap");

    $.ajax({
        type: "POST",
        url: "/saveVideo/",
        data: { json_str: JSON.stringify(snap) },
        success: function(response) {},
        error: function() {
            alert("Chiamata fallita!!!");
        }
    });
    snap += 1;

    if (snap % 2 != 0) {
        navigator.mediaDevices.getUserMedia({
            audio: false,
            video: true
        }).then(function(stream) {
            // Display a live preview on the video element of the page
            setSrcObject(stream, video);

            // Initialize the recorder
            recorder = new RecordRTCPromisesHandler(stream, {
                mimeType: 'video/webm',
                bitsPerSecond: 128000
            });

            // Start recording the video
            recorder.startRecording().then(function() {
                console.info('Recording video ...');
            }).catch(function(error) {
                console.error('Cannot start video recording: ', error);
            });

            // release stream on stopRecording
            recorder.stream = stream;
        });

    } else if (snap % 2 == 0) {
        recorder.stopRecording().then(function() {
            console.info('stopRecording success');

            // Retrieve recorded video as blob and display in the preview element
            var blob = recorder.getBlob();

            // Stop the device streaming
            recorder.stream.stop();
            location.reload()
        });
    }
}

// https://hackernoon.com/how-to-use-javascript-closures-with-confidence-85cd1f841a6b
// closure; store this in a variable and call the variable as function
// eg. var takeSnapshotUI = createClickFeedbackUI();
// takeSnapshotUI();

function createClickFeedbackUI() {

    // in order to give feedback that we actually pressed a button. 
    // we trigger a almost black overlay
    var overlay = document.getElementById("video_overlay"); //.style.display;

    // sound feedback
    var sndClick = new Howl({ src: ['snd/click.mp3'] });

    var overlayVisibility = false;
    var timeOut = 80;

    function setFalseAgain() {
        overlayVisibility = false;
        overlay.style.display = 'none';
    }

    return function() {

        if (overlayVisibility == false) {
            sndClick.play();
            overlayVisibility = true;
            overlay.style.display = 'block';
            setTimeout(setFalseAgain, timeOut);
        }

    }
}