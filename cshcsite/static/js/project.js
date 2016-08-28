// Ref: http://www.abeautifulsite.net/blog/2011/11/detecting-mobile-devices-with-javascript/
var isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};

function parseParams(){
    // If the team context is provided, store it in a cookie
    var teams = window.location.search.match(/team=[\w\d]*/i);
    if (teams) {
        var team = teams[0].split('=')[1]
        Cookies.set('cshc_team', team.toLowerCase(), { expires: 365 });
    }
};

// Ref: http://stackoverflow.com/questions/1108693/is-it-possible-to-register-a-httpdomain-based-url-scheme-for-iphone-apps-like/2391031#2391031
function applink(fail){
    return function(){
        var clickedAt = +new Date;
        // During tests on 3g/3gs this timeout fires immediately if less than 500ms.
        setTimeout(function(){
            // To avoid failing on return to MobileSafari, ensure freshness!
            alert("Timed out")
            if (+new Date - clickedAt < 2000){
                window.location = fail;
            }
        }, 500);
    };
}

function scrollToTop(element, parent){
    var topOffset = 0;
    if ($('.navbar-fixed-top').length) {
        topOffset += 69 //$('#top-nav').height();
    }
    $(parent).animate({ scrollTop: $(element).offset().top - $(parent).offset().top - topOffset }, { duration: 'slow', easing: 'swing'});
}

function ajax_load(url, tag_id) {
    if (url != "") {
        $.ajax({
            url: url, cache: false, success: function (result) {
                $("#" + tag_id).html(result);
            }
        });
    }
    else {
        $("#" + tag_id).html("<div class='loading-error'><div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Could not load dynamic content</div></div>");
    }
}

function expand(id) {
    $(".accordion-body").collapse('hide')
    $("#collapse" + id).collapse('show')
}

$(function(){
    parseParams();

    $(".pop").each(function() {
        var $pElem= $(this);
        $pElem.popover(
            {
                html: true,
                trigger: 'manual',
                title: getPopTitle($pElem.attr("id")),
                content: getPopContent($pElem.attr("id"))
            }
        );
    });

    $(".pop").click(function() {
        var $pElem= $(this);
        $(".pop").each(function() {
            $currentPop= $(this);
            if($currentPop.prop("id") != $pElem.prop("id")) {
                $currentPop.popover('hide');
            }
        });
        $pElem.popover('toggle');
    });

});

function getPopTitle(target) {
    return $("#" + target + "_content > div.popTitle").html();
};

function getPopContent(target) {
    return $("#" + target + "_content > div.popContent").html();
};
