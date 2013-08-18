$(document).ready(function() {
    /**
     * Binding to hashChange method
     * 
     * @return {[type]} [description]
     */
    $(window).hashchange(function() {
        /**
         * Hash
         * 
         * @type {[type]}
         */
        var hash = document.location.hash;
        /**
         * Location
         * 
         * @type {[type]}
         */
        var location = hash.substring(1);

        /**
         * Parts of location
         * 
         * @type {[type]}
         */
        var parts = location.split("|");

        /**
         * Analytic
         * 
         * @type {[type]}
         */
        var analytic = null;

        /**
         * Feature (+ target_price)
         * @type {[type]}
         */
        var feature = null;

        /**
         * Chart object
         * @type {[type]}
         */
        var chart_element = null;

        /**
         * If we have more than one part, this means, that the first part is the analytic slug
         *
         * and the second part is the page
         * - target_price
         * - feature in analysis page
         */
        if (parts.length > 1) {
            analytic = parts[0];
            feature = parts[1];
            
            /**
             * Grab the analytic
             * 
             * @type {[type]}
             */
            if (analytic === undefined) {
                var analytic = $('.ta').attr('data-analytic');
            }
            
            /**
             * Grab the ticker
             * @type {[type]}
             */
            var ticker = $('.ta').attr('data-ticker');
            if (ticker === undefined) {
                ticker = null;
            }

            /**
             * Which page we are currently in
             */
            if (feature != 'target_prices') {
                if ($("a.ta").hasClass("active")) {
                    /**
                     * Switch the active tabs
                     */
                    $("a.ta").removeClass("active");
                    $("a.an").addClass("active");

                    /**
                     * Changing the content 
                     * @return {[type]}
                     */
                    $('.inner_target_prices').animate({
                        'opacity': 0
                    }, 50, function() {
                        $(this).addClass('hidden');
                        $('.inner_content').removeClass('hidden').css('opacity', 0);
                        $('.inner_content').animate({
                            'opacity': 1
                        }, 100);
                    });

                    /**
                     * Select the analytic
                     */
                    chart_element = $("#chart svg [name=" + analytic + "]");
                    console.log('Chart element:', chart_element);
                    if (!chart_element.hasClass('active')) {
                        console.log('Chart element is not active');
                        chart_element.attr('fill', '#e95201').attr('selected', 1);
                    }

                    $(".analyser li").each(function(index, element) {
                        if ($(element).attr('name') == analytic) {
                            $(element).attr('class', 'active');
                        } else {
                            $(element).attr('class', 'passive');
                        }
                    });

                    /**
                     * Select the feature
                     * @type {[type]}
                     */
                    var active_feature = $('.analyse_menu a.active');
                    if (active_feature.length === 0) {
                        $('.analyse_menu div:first-child a').trigger('click');
                        active_feature = $('.analyse_menu a.active');
                    }
                    active_feature = active_feature.parent('div').attr('name');
                }
            }
        }
    });
})