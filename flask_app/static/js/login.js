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
        alert(name)
        $.ajax({
            url: '/registration',
            type: 'POST',
            data: { 'name': name, 'pass': md5(pass), 'email': email, 'azienda': azienda, 'admin': admin },
            success: function(response) {
                window.location.replace("/");
            }
        })

    });



    $(document).on("click", ".app__logout", function(e) {
        if (animating) return;
        $(".ripple").remove();
        animating = true;
        var that = this;
        $(that).addClass("clicked");
        setTimeout(function() {
            $app.removeClass("active");
            $login.show();
            $login.css("top");
            $login.removeClass("inactive");
        }, logoutPhase1 - 120);
        setTimeout(function() {
            $app.hide();
            animating = false;
            $(that).removeClass("clicked");
        }, logoutPhase1);
    });

});