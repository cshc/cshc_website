
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



    // $('.po').popover()
    // $('.tt').tooltip()
});

function getPopTitle(target) {
    return $("#" + target + "_content > div.popTitle").html();
};

function getPopContent(target) {
    return $("#" + target + "_content > div.popContent").html();
};
