/**
 * Loader
 */
var loader = (function() {

    var horizontal_slider_top_offset = 0;
    var horizontal_slider = 0;
    var last_offset = 0;
    var page = 0;
    var loading = false;
    var type = 'grid';
    var sort_direction = null;
    var sort_slug = null;

    return {

        document_ready: function() {
            if ($('.horizontal_slider').length !== 0) {
                horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
            }
            loader.target_prices();
        },
        /**
         * Loading sorted 
         * 
         * @param  {[type]} slug      [description]
         * @param  {[type]} direction [description]
         * @return {[type]}           [description]
         */
        sorted: function(_sort_slug, _sort_direction, _page) {
            /**
             * Check input
             */
            if (_sort_slug === undefined) {
                if (sort_slug === null) {
                    sort_slug = 'accuracy';
                }
            } else {
                sort_slug = _sort_slug;
            }
            if (_sort_direction === undefined) {
                if (sort_direction === null) {
                    sort_direction = 'down';
                }
            } else {
                sort_direction = _sort_direction;
            }
            if (_page !== undefined) {
                page = _page;
            }
            type = 'list';

            $.getJSON('/api/target_prices/' + sort_slug + '/' + sort_direction + '/' + page + '/', function(data) {
                if (data.length < 1) {
                    loading = true;
                } else {
                    render.target_prices(data);
                    loading = false;
                }
            });
            page = page + 1;
        },
        /**
         * Load listing of target prices
         * 
         * @param  {[type]} _page [description]
         * @return {[type]}       [description]
         */
        target_prices: function(_page) {
            if (_page !== undefined) {
                page = _page;
            }
            type = 'grid';
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
                /* Check the view */
                if (type == 'grid') {
                    loader.target_prices();
                } else {
                    loader.sorted();
                }
            }
        }
    };
})();

$(document).ready(loader.document_ready);
$(window).scroll(loader.scroll_happend);