/**
 * Loader
 */
var loader = (function() {

    var horizontal_slider_top_offset = 0;
    var horizontal_slider = 0;
    var last_offset = 0;
    var page = 0;
    var loading = false;

    return {

        document_ready: function() {
            console.log('Loader');
            if ($('.horizontal_slider').length !== 0) {
                horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
            }
            loader.target_prices();
        },
        target_prices: function() {
            $.getJSON('/api/target_prices/' + page + '/', function(data) {
                /**
                 * No more data from the server -- kill the loader
                 */
                if (data.length < 1) {
                    loading = true;
                } else {
                    render.target_prices(data);
                    loading = false;
                }
            });
            page = page + 1;
        },

        scroll_happend: function() {
            if ($('.target_price_list > li:nth-last-of-type(1)').offset() !== undefined) {
                this.last_offset = $('.target_price_list > li:nth-last-of-type(1)').offset().top;
            }
            if ( $(window).scrollTop() + $(window).height() >= this.last_offset && loading === false ) {
                loading = true;
                loader.target_prices();
            }
        }
    };
})();

$(document).ready(loader.document_ready);
$(window).scroll(loader.scroll_happend);