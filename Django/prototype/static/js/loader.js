/**
 * Loader
 */
var loader = (function() {

    var horizontal_slider_top_offset = 0;
    var horizontal_slider = 0;
    var last_offset = 0;
    var page = 0;
    var loading = false;
    var config = {
        'type': 'grid', // grid or list
        'ticker': null,
        'analytic': null,
        'sort': { // Sorting matters
            'slug': null,
            'direction': null
        },
        'page': 0 // page number
    };
    var sort_direction = null;
    var sort_slug = null;

    return {

        document_ready: function(_autoload) {
            if (_autoload === undefined) {
                _autoload = true;
            }
            if ($('.horizontal_slider').length !== 0) {
                horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
            }
            if (_autoload) {
                loader.target_prices();
            }
        },

        reset_page_number: function() {
            config.page = 0;
        },

        reset_sort: function() {
            config.sort = {
                'slug': null,
                'direction': null
            };
        },

        /**
         * Load listing of target prices
         * 
         * @param  {[type]} _page [description]
         * @return {[type]}       [description]
         */
        target_prices: function(_config) {
            if (_config !== undefined) {
                config = _config;
            }

            console.log(config);

            url = null;
            if (config.ticker !== null && config.sort.slug !== null && config.sort.direction !== null) {
                url = '/api/target_prices/tickers/' + config.ticker + '/' + config.sort.slug + '/' + config.sort.direction + '/' + config.page + '/';
            } else if (config.anlaytic !== null && config.sort.slug !== null && config.sort.direction !== null) {
                url = '/api/target_prices/analytics/' + config.anlaytic + '/' + config.sort.slug + '/' + config.sort.direction + '/' + config.page + '/';
            } else if (config.analytic !== null) {
                /**
                 * Analytic target prices
                 * 
                 * @type {String}
                 */
                url = '/api/target_prices/analytics/' + config.analytic + '/' + config.page + '/';
            } else if (config.ticker !== null) {
                /**
                 * Ticker target prices
                 * 
                 * @type {String}
                 */
                url = '/api/target_prices/tickers/' + config.ticker + '/' + config.page + '/';
            } else if (config.sort.slug !== null && config.sort.direction !== null) {
                /**
                 * Sorted target prices
                 * 
                 * @type {String}
                 */
                url = '/api/target_prices/' + config.sort.slug + '/' + config.sort.direction + '/' + config.page + '/';
            } else {
                /**
                 * Default 
                 * 
                 * @type {String}
                 */
                url = '/api/target_prices/' + config.page + '/';
            }

            $.getJSON(url, function(data) {
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
            if (config.page === 0) {
                console.log('Reload now value from loader');
                render.now_reload_enable();
            } else {
                render.now_reload_disable();
            }
            config.page = config.page + 1;
        },

        scroll_happend: function() {
            if ($('.target_price_list > li:nth-last-of-type(1)').offset() !== undefined) {
                this.last_offset = $('.target_price_list > li:nth-last-of-type(1)').offset().top;
            }
            if ( $(window).scrollTop() + $(window).height() >= this.last_offset && loading === false ) {
                console.log(config);
                loading = true;
                /* View is managed by render */
                loader.target_prices();
            }
        }
    };
})();