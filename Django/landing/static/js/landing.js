$(document).ready(function() {

    $('#id_email').val($('.id_email').html());
    $('#id_email').css({'color': '#bdbdbd'});

    $('body').on('click', function(event) {
        // console.log(event.target);
        if ($(event.target).attr('id') == 'id_email') {
            // console.log($('#id_email').val());
            if ($('#id_email').val() === $('.id_email').html()) {
                $('#id_email').val('');
                $('#id_email').css({'color': '#333'});
            }
        } else {
            if ($('#id_email').length > 0) {
                if ($('#id_email').val().length < 1) {
                    $('#id_email').css({'color': '#bdbdbd'});
                    $('#id_email').val($('.id_email').html());
                }
            }
            
        }
    });
});

function fbs_click(width, height) {
    var leftPosition, topPosition;
    //Allow for borders.
    leftPosition = (window.screen.width / 2) - ((width / 2) + 10);
    //Allow for title and status bars.
    topPosition = (window.screen.height / 2) - ((height / 2) + 50);
    var windowFeatures = "status=no,height=" + height + ",width=" + width + ",resizable=yes,left=" + leftPosition + ",top=" + topPosition + ",screenX=" + leftPosition + ",screenY=" + topPosition + ",toolbar=no,menubar=no,scrollbars=no,location=no,directories=no";
    u = 'http://anavest.com';
    t = document.title;
    window.open('http://www.facebook.com/sharer.php?u='+encodeURIComponent(u)+'&t='+encodeURIComponent(t),'sharer', windowFeatures);
    return false;
}