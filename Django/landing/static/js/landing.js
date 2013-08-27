$(document).ready(function() {

    $('input[name="email"]').each(function() {
        $(this).val($('.id_email').html())
    });

    $('input[name="email"]').css({'color': '#bdbdbd'});
    $('body').on('click', function(event) {
        // console.log(event.target);
        if ($(event.target).attr('name') == 'email') {
            if ($(event.target).val() === $('.id_email').html()) {
                $(event.target).val('');
                $(event.target).css({'color': '#333'});
            }
            // if ($('#id_email').val() === $('.id_email').html()) {
            //     $('#id_email').val('');
            //     $('#id_email').css({'color': '#333'});
            // }
        } else {
            $('input[name="email"]').each(function() {
                if ($(this).length > 0) {
                    if ($(this).val().length < 1) {
                        $(this).css({'color': '#bdbdbd'});
                        $(this).val($('.id_email').html());
                    }
                }
            });
            
            // if ($('#id_email').length > 0) {
            //     if ($('#id_email').val().length < 1) {
            //         $('#id_email').css({'color': '#bdbdbd'});
            //         $('#id_email').val($('.id_email').html());
            //     }
            // }
        }
    });
    /**
     * Carousel
     */
    if ($('.carousel').length > 0) {
        $('.carousel').carouFredSel({
            direction: "right",
            auto: false,
            width: "600",
            scroll: {
                fx: 'fade',
                easing: "linear"
            },
            infinite: false,
            prev: {
                button: '#carousel_prev',
                key: 'left'
            },
            next: {
                button: '#carousel_next',
                key: 'right'
            },
            pagination: '#carousel_pagination'
        });
    }
});

function fbs_click(width, height) {
    var leftPosition, topPosition;
    var u = null;
    //Allow for borders.
    leftPosition = (window.screen.width / 2) - ((width / 2) + 10);
    //Allow for title and status bars.
    topPosition = (window.screen.height / 2) - ((height / 2) + 50);
    var windowFeatures = "status=no,height=" + height + ",width=" + width + ",resizable=yes,left=" + leftPosition + ",top=" + topPosition + ",screenX=" + leftPosition + ",screenY=" + topPosition + ",toolbar=no,menubar=no,scrollbars=no,location=no,directories=no";
    var u = 'http://anavest.com';
    var t = document.title;
    window.open('http://www.facebook.com/sharer.php?u='+encodeURIComponent(u)+'&title='+encodeURIComponent(t), 'facebook', windowFeatures);
    return false;
}

function twt_click() {
    var leftPosition, topPosition;
    var u = null;
    var width = 600;
    var height = 600;
    //Allow for borders.
    leftPosition = (window.screen.width / 2) - ((width / 2) + 10);
    //Allow for title and status bars.
    topPosition = (window.screen.height / 2) - ((height / 2) + 50);
    var windowFeatures = "status=no,height=" + height + ",width=" + width + ",resizable=yes,left=" + leftPosition + ",top=" + topPosition + ",screenX=" + leftPosition + ",screenY=" + topPosition + ",toolbar=no,menubar=no,scrollbars=no,location=no,directories=no";
    u = 'Know who to listen to in the financial world';
    window.open('https://twitter.com/share?url=http://avanest.com/&lang=en&text=' + encodeURIComponent(u), 'twitter', windowFeatures);
    return false;
}