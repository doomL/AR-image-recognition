$(document).ready(function() {

    var animating = false,
        submitPhase1 = 1100,
        submitPhase2 = 400,
        logoutPhase1 = 800,
        $login = $(".login"),
        $app = $(".app");

    function ripple(elem, e) {
        $(".ripple").remove();
        var elTop = elem.offset().top,
            elLeft = elem.offset().left,
            x = e.pageX - elLeft,
            y = e.pageY - elTop;
        var $ripple = $("<div class='ripple'></div>");
        $ripple.css({ top: y, left: x });
        elem.append($ripple);
    };

    $(document).on("click", "#login", function(e) {
        var name = $('#name').val()
        var pass = $('#pass').val()
        if (animating) return;
        animating = true;
        var that = this;
        ripple($(that), e);
        /*$(that).addClass("processing");
        setTimeout(function() {
            $(that).addClass("success");
            setTimeout(function() {
                $app.show();
                $app.css("top");
                $app.addClass("active");
            }, submitPhase2 - 70);
            setTimeout(function() {
                $login.hide();
                $login.addClass("inactive");
                animating = false;
                $(that).removeClass("success processing");
            }, submitPhase2); 
    }, submitPhase1);*/
        console.log(name)
        console.log(pass)
        $.ajax({
            url: '/login1',
            type: 'POST',
            data: { 'name': name, 'pass': md5(pass) },
            success: function(response) {
                iziToast.success({
                    title: 'OK',
                    message: 'Successfully inserted record!',
                });
                window.location.replace("/");
            },
            error: function(response) {
                //json = JSON.parse(response);
                iziToast.error({
                    title: 'Error',
                    message: 'Illegal operation',
                });
                window.location.replace("/login");
            }
        });
    });

    $(document).on("click", "#registration", function(e) {
        var name = $('#name').val()
        var pass = $('#pass').val()
        var email = $('#email').val()
        var azienda = $('#azienda').val()
        var admin = $('#admin').val()

        if (animating) return;
        animating = true;
        var that = this;
        ripple($(that), e);
        /*$(that).addClass("processing");

        setTimeout(function() {
            $(that).addClass("success");
            setTimeout(function() {
                $app.show();
                $app.css("top");
                $app.addClass("active");
            }, submitPhase2 - 70);
            setTimeout(function() {
                $login.hide();
                $login.addClass("inactive");
                animating = false;
                $(that).removeClass("success processing");
            }, submitPhase2);
        }, submitPhase1);*/
        $.ajax({
            url: '/registration',
            type: 'POST',
            data: { 'name': name, 'pass': md5(pass), 'email': email, 'azienda': azienda, },
            success: function(response) {
                iziToast.success({
                    title: 'OK',
                    message: 'Successfully inserted record!',
                });
                window.location.replace("/login");
            },
            error: function(response) {
                //json = JSON.parse(response);
                iziToast.error({
                    title: 'Error',
                    message: 'Illegal operation',
                });
                window.location.replace("/signUp");
            }
        });

    });

    $("#azienda").keyup(function (event) {
        if (event.keyCode === 13) {
            $("#registration").click();
        }
    });


    $("#pass").keyup(function (event) {
        if (event.keyCode === 13) {
            $("#login").click();
        }
    });


});