// Client-side logic for handling bulk addition of training sessions

$(function(){

    dt = new Date();
    $('#id_datetime_0').val(dt.getFullYear() + '-' + (dt.getMonth() + 1) + '-' + ("00" + dt.getDate()).slice (-2));
    $('#id_datetime_1').val("19:00");

    $('input[type=radio][name=repeat_option]').change(function() {
        if (this.value == 'M') {
            $('#id_repeat_count').prop('disabled', false);
            $('#id_repeat_until').prop('disabled', true);
        }
        else if (this.value == 'U') {
            $('#id_repeat_count').prop('disabled', true);
            $('#id_repeat_until').prop('disabled', false);
        }
    });

    $('#id_repeat').change(function() {
        $('#repeat_config').toggle();
    });

    $("#id_repeat_option_0").prop("checked", true).trigger('change');
});