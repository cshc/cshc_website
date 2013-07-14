
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



