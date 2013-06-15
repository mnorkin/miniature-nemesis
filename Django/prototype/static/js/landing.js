$(document).ready(function() {

    $('#id_email').val($('.id_email').html());
    $('#id_email').css({'color': '#bdbdbd'});

    $('body').on('click', function(event) {
        console.log(event.target);
        if ($(event.target).attr('id') == 'id_email') {
            console.log($('#id_email').val());
            if ($('#id_email').val() === $('.id_email').html()) {
                $('#id_email').val('');
                $('#id_email').css({'color': '#333'});
            }
        } else {
            if ($('#id_email').val().length < 1) {
                $('#id_email').css({'color': '#bdbdbd'});
                $('#id_email').val($('.id_email').html());
            }
        }
    });
});