jQuery(document).ready(function($){
  var deviceAgent = navigator.userAgent.toLowerCase();
  
  if (deviceAgent.match(/(iphone|ipod|ipad)/)) {
    $(".page-wrapper").removeClass("toggled");
  }
  
  if (deviceAgent.match(/android/)) {
    $(".page-wrapper").removeClass("toggled");
  }
  
  if (deviceAgent.match(/blackberry/)) {
    $(".page-wrapper").removeClass("toggled");
  }
  
  if (deviceAgent.match(/(symbianos|^sonyericsson|^nokia|^samsung|^lg)/)) {
    $(".page-wrapper").removeClass("toggled");
  }
  
});

var video = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}

jQuery(function ($) {

  $(".sidebar-dropdown > a").click(function () {
    $(".sidebar-submenu").slideUp(200);
    if (
      $(this)
        .parent()
        .hasClass("active")
    ) {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .parent()
        .removeClass("active");
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .next(".sidebar-submenu")
        .slideDown(200);
      $(this)
        .parent()
        .addClass("active");
    }
  });
  
  $("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");
  });
  $("#show-sidebar").click(function () {
    $(".page-wrapper").addClass("toggled");
  });




});