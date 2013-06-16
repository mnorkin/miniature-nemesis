/**
 * Render
 */

var render = (function() {

    /**
     * Target price template
     * 
     * @type {[type]}
     */
    var target_price_template = null;

    /**
     * List type
     * 
     * @type {[type]}
     */
    var list_type = null;

    /**
     * maximum value of accuracy
     * @type {Number}
     */
    var MAX_ACCURACY = 100;
    /**
     * minimum value of accuracy
     *
     * value calculated, based on grid type listing
     * @type {Number}
     */
    var MIN_ACCURACY = 3.5;
    /**
     * maximum value of profitability
     * @type {Number}
     */
    var MAX_PROFITABILITY = 100;
    /**
     * minimum value of profitability
     *
     * value calculated, based on grid type listing
     * @type {Number}
     */
    var MIN_PROFITABILITY = 3.5;
    /**
     * maximum value of reach time
     * @type {Number}
     */
    var MAX_REACH_TIME = 250;
    /**
     * minimum value of reach time
     *
     * value calculated, based on grid type listing
     * @type {Number}
     */
    var MIN_REACH_TIME = 8;
    /**
     * Width of the graph, then the listing type is list
     * @type {Number}
     */
    var WIDTH_OF_LIST_TYPE = 135;
    /**
     * Width of the graph, then the listing type is grid
     * @type {Number}
     */
    var WIDTH_OF_GRID_TYPE = 356;

    return {

        document_ready: function() {
            $("script").each(function() {
                var new_replaced_txt = $(this).text().replace(/\[\[/g, "{{").replace(/\]\]/g, "}}");
                $(this).text(new_replaced_txt);
            });
            list_type = 'grid';
        },

        /**
         * Render target prices
         * @param  {[type]} data [description]
         * @return {[type]}      [description]
         */
        target_prices: function(data) {
            var i = 0;
            var j = 0;
            var element = null;
            var graph_data = null;
            target_price_template = $("#target_price_template").html();
            for (i=0; i < data.length; i++) {
                element = Mustache.to_html(target_price_template, data[i]);
                $("#target-price-list").append(element);
                render.change(
                    data[i].hash + '01',
                    data[i].change.value
                );
                for (j=0; j < data[i].features.length; j++) {
                    render.feature(
                        data[i].hash + '01',
                        data[i].features[j].value,
                        data[i].features[j].slug
                    );
                }
            }
            render.tooltips();
        },
        /** 
         * Filtering the minimum value of the feature
         * @param  {[type]} value   [description]
         * @param  {[type]} feature [description]
         * @return {[type]}         [description]
         */
        filter_minimum_data: function(value, feature) {
            /**
             * Scaling factor defines the difference between the grid type of listing
             * and list type of listing
             *
             * @type {[type]}
             */
            var scaling_factor = WIDTH_OF_GRID_TYPE / WIDTH_OF_LIST_TYPE;

            switch (feature) {
                case 'accuracy':
                    if (value < MIN_ACCURACY && list_type == 'grid') {
                        value = MIN_ACCURACY;
                    } else if (value < MIN_ACCURACY * scaling_factor && list_type == 'list') {
                        value = MIN_ACCURACY * scaling_factor;
                    }
                    break;
                case 'profitability':
                    if (value < MIN_PROFITABILITY && list_type == 'grid') {
                        value = MIN_PROFITABILITY;
                    } else if (value < MIN_PROFITABILITY * scaling_factor && list_type == 'list') {
                        value = MIN_PROFITABILITY * scaling_factor;
                    }
                    break;
                case 'reach_time':
                    if (value < MIN_REACH_TIME && list_type == 'grid') {
                        value = MIN_REACH_TIME;
                    } else if (value < MIN_REACH_TIME * scaling_factor && list_type == 'list') {
                        value = MIN_REACH_TIME * scaling_factor;
                    }
            }
            return value;
        },

        /**
         * Filtering the maximum value of the feature
         * @param  {[type]} value   [description]
         * @param  {[type]} feature [description]
         * @return {[type]}         [description]
         */

        filter_maximum_data: function(value, feature) {
            switch (feature) {
                case 'accuracy':
                    if (value > MAX_ACCURACY) {
                        value = MAX_ACCURACY;
                    }
                    break;
                case 'profitability':
                    if (value > MAX_PROFITABILITY) {
                        value = MAX_PROFITABILITY;
                    }
                    break;
                case 'reach_time':
                    if (value > MAX_REACH_TIME) {
                        value = MAX_REACH_TIME;
                    }
            }
            return value;
        },

        /**
         * Filtering the input data to the graphs
         * @param  {[type]} value   [description]
         * @param  {[type]} feature [description]
         * @return {[type]}         [description]
         */

        filter_graph_data: function(value, feature) {
            /**
             * Storing the original value to be able to restore the sign of the value
             * 
             * @type {[type]}
             */
            var initial_value = value;
            /**
             * Rounding to perform the maximum/minimum part
             * 
             * @type {[type]}
             */
            value = Math.abs(value);

            value = render.filter_minimum_data(value, feature);
            value = render.filter_maximum_data(value, feature);

            /**
             * Checking if we have negative or positive value from the start
             */
            if (initial_value < 0) {
                return -value;
            }
            /**
             * Return appropriate value otherwise
             */
            return value;
        },

        /**
         * Returning the maximum value of the feature
         * @param  {[type]} feature [description]
         * @return {[type]}         [description]
         */

        filter_maximum_value: function(feature) {
            var value = 0;
            switch (feature) {
                case 'accuracy':
                    value = render.filter_maximum_data(10000, feature);
                    break;
                case 'profitability':
                    value = render.filter_maximum_data(10000, feature);
                    break;
                case 'reach_time':
                    value = render.filter_maximum_data(10000, feature);
            }
            return value;
        },

        /**
         * Generating the pies of data
         * @param  {[type]} id      [description]
         * @param  {[type]} dataset [description]
         * @param  {[type]} posName [description]
         * @return {[type]}         [description]
         */

        feature: function(id, dataset, posName) {

            /**
             * Check the list type
             */
            if (typeof(list_type) == "undefined") {
                list_type = 'grid';
            }

            /**
             * The dataset value, injecting to the text field in the tooltip
             * @type array
             */
            var dataset_txt_value = dataset;

            /**
             * Boolean variable to indicate if the property is negative or not
             * 
             * @type {Boolean}
             */
            var negative = false;

            /**
             * Maximum value of the graph
             * @type int
             */
            var max_value = render.filter_maximum_value(posName);

            /**
             * Width of the drawing graph
             * @type {Number}
             */
            var width = 0;
            if (list_type == 'list') {
                width = 135;
            } else {
                width = 356;
            }

            if (dataset_txt_value < 0) {
                negative = true;
            }

            // Filtering the data for minimum values
            dataset = render.filter_graph_data(dataset, posName);

            if (id !== null) {
                dataset = [dataset];

                /**
                 * Defined gradients
                 * @type {Object}
                 */
                var gradiends = {
                    'accuracy': '#8dc3b2',
                    'profitability': '#aa8dc3',
                    'reach_time': '#6189b8',
                    'negative': '#ea251d'
                };

                /**
                 * X domain scale
                 * @type {[type]}
                 */
                var x = null;
                if (negative === true) {
                    x = d3.scale.linear()
                        .domain([0, -max_value])
                        .range([0, width]);
                } else {
                    x = d3.scale.linear()
                        .domain([0, max_value])
                        .range([0, width]);
                }

                /**
                 * Making the SVG element
                 * @type {[type]}
                 */
                var chart = d3.selectAll("#" + id + ' .' + posName)
                    .append('svg')
                    .attr('width', width)
                    .attr('height', '20')
                    .append('g');

                /**
                 * The vertical line
                 */
                var y = 0;
                if (negative === true) {
                    posName = 'negative';
                }

                chart.selectAll('rect')
                    .data(dataset)
                    .enter().append('rect')
                    .attr('height', 11)
                    .attr('y', y)
                    .attr('fill', gradiends[posName])
                    .attr('rx', 5)
                    .attr('ry', 5)
                    .attr('transform', function() {
                        if (negative === true) {
                            return 'translate('+width+',11) rotate(180)';
                        }
                    })
                    .attr('txt', function(d, i) {
                        if (posName == 'reach_time') {
                            return dataset_txt_value + ' days';
                        } else {
                            return dataset_txt_value + ' %';
                        }
                    })
                    .transition().duration(1500).attr('width', x)
                    .text(String);

                /**
                 * The circle
                 */
                chart.append('circle')
                    .attr('fill', '#000')
                    .style('opacity', '0.3')
                    .data(dataset)
                    .attr('transform', function() {
                        if (negative === true) {
                            return 'translate('+width+',11) rotate(180)';
                        }
                    })
                    .attr('cy', 5.5)
                    .transition().duration(1500)
                    .attr('r', 3.5)
                    .attr('cx', function(d, i) {
                        if (negative === true) {
                            return x(d)-6;
                        }
                        return x(d)-6;
                    });
            } else {
                return;
            }
        },


        /**
         * Display change graph
         * 
         * @param  {[type]} id    [description]
         * @param  {[type]} value [description]
         * @return {[type]}       [description]
         */
        change: function(id, value) {
            if (typeof(list_type) != "undefined" && list_type == 'list') {
                return; // ???
            }

            var percent = Math.abs(value);
            percent = Math.min(percent, 100);
            var width = 82,
                height = 82,
                radius = Math.min(width, height) / 2,
                angle = 360 * percent / 100;
            var fill_color = (value > 0) ? "#b9d240" : "#e72727";

            var arc = d3.svg.arc()
                .innerRadius(35)
                .outerRadius(35)
                .startAngle(0)
                .endAngle(function(d) {
                return d * (Math.PI / 180);
            });

            var svg = d3.select("#" + id + ' .circle').append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

            // draw arc with 0 value
            var path = svg.append('path')
                .data([0])
                .attr("stroke", fill_color)
                .attr("fill", fill_color)
                .attr('stroke-width', 11)
                .attr('stroke-linejoin', 'round')
                .attr("d", arc)
                .each(function(d) {
                this._current = d;
            }); // store the initial values;

            // animate arc with real values
            path = path.data([angle])
                .transition().duration(1500)
                .attrTween("d", function(a) {
                var i = d3.interpolate(this._current, a);
                var k = d3.interpolate(arc.outerRadius()(), 35);
                this._current = i(0);
                return function(t) {
                    return arc.innerRadius(35).outerRadius(k(t))(i(t));
                };
            });

            var get_circle_points = function(radius, angle) {
                var x = radius * Math.sin(angle * Math.PI / 180);
                var y = radius * -Math.cos(angle * Math.PI / 180);
                return [x, y];
            };

            // circle at start and in the end, for safari and mac's stroke-linejoint bug (roundness).
            if (percent > 1) {
                d3.select("#" + id + ' .circle svg').append('g').selectAll('circle')
                    .data([0, angle - 1.2]).enter()
                    .append('circle')
                    .attr('fill', fill_color)
                    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
                    .attr('cx', function(d, i) {
                    return get_circle_points(35, d)[0];
                })
                    .attr('cy', function(d, i) {
                    return get_circle_points(35, d)[1];
                })
                    .transition().delay(function(d, i) {
                    return i * 1000;
                })
                    .attr('r', 5.1);
            }

            // small dark circle point
            if (percent > 1) {
                d3.select("#" + id + ' .circle svg')
                    .append('circle')
                    .attr('fill', '#000')
                    .attr('style', 'opacity:0.3;')
                    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
                    .attr('cx', function() {
                    return get_circle_points(35, angle - 2)[0];
                })
                    .attr('cy', function() {
                    return get_circle_points(35, angle - 2)[1];
                })
                    .transition().delay(1000).duration(500)
                    .attr('r', 3.5);
            }
        },
        /**
         * [binds_for_target_price_list description]
         * @return {[type]} [description]
         */
        tooltips: function() {
            /* Tooltip (percent info box) */
            $('.chart .bar rect').hover(function() {
                var obj = $(this);
                var chart = obj.closest('.chart');
                var tooltip = chart.children('.bar_tooltip');

                tooltip.text(obj.attr('txt')).css({
                    display: 'block',
                    opacity: 0,
                    width: 'auto'
                });
                var width = tooltip.width();

                /*var bar_cont_width = ($('.latest_target_prices.list.hidden').length) ? 347 : 133;
                var left = Math.min(obj.offset().left - chart.offset().left + bar_cont_width - width +,
                obj.offset().left - chart.offset().left + parseInt(obj.attr('width'), 10) -2.7); */

                var top = obj.offset().top - chart.offset().top - 3.8;
                var left = obj.offset().left - chart.offset().left + parseInt(obj.attr('width'), 10) - 2.7;

                // These kind of expressions are really hard to understand
                var speed = (
                    parseInt(tooltip.css('top'), 10) == parseInt(top, 10) &&
                    parseInt(tooltip.css('left'), 10) == parseInt(left, 10)) ? 0 : 200;

                tooltip.css({
                    top: top,
                    left: left,
                    width: 0,
                    opacity: 1
                }).animate({
                    width: width
                }, speed);

                if (chart.children('.tooltip_point').length === 0) {
                    chart.append('<span class="tooltip_point"></span>');
                }
                chart.children('.tooltip_point').css({
                    left: (left - 4),
                    top: (top + 5),
                    display: 'block'
                });

            }, function() {});

            $('.chart').hover(function() {}, function() {
                $('.bar_tooltip').fadeOut(150);
                $('.tooltip_point').fadeOut(150);
            });

            // long company names moving
            $('.title .entry').hover(function() {
                var obj = $(this);
                obj.find('.goust').text(obj.find('.text .slid').text());
                var left = Math.min(0, (165 - obj.find('.goust').width()));
                obj.find('.text .slid').animate({
                    'left': left
                }, (left * -15));
            }, function() {
                $(this).find('.text .slid').stop().css({
                    'left': 0
                });
            });

            $('.title .entry').click(function() {
                location.href = $(this).find('a').attr('href');
            });

            $('.latest_target_prices .toggle').unbind('click').click(
                render.change_target_prices_list
            );
            $('.title.list .pre_info span a').unbind('click').click(
                render.sort_target_prices
            );

            // hide company name if it's company page or bank page
            if (
                $('.inner_target_prices').attr('type') !== undefined &&
                $('.latest_target_prices').length !== 0) {
                var obj, who = $('.inner_target_prices').attr('type');
                $('.inner_target_prices').removeAttr('type');
                $('#target-price-list .entry').each(function() {
                    obj = $(this);
                    if (who == 'ticker') {
                        obj.find('.text .slid').text(obj.find('.analytic').text());
                    }
                    obj.find('.analytic').text(obj.find('.date').text());
                });
            }
            // to see last target price date
            $('.target_price_list').css('padding-bottom',
                $(window).height() - $('.title .entry').outerHeight() - 77);
        },

        /**
         * Sorting target prices
         * 
         * @return {[type]} [description]
         */
        sort_target_prices: function() {
            var data = Object;
            var obj = $(this);
            if (obj.hasClass('active')) {
                return; // This is bad style
            }
            $('.title.list .pre_info span a').removeClass('active');
            obj.addClass('active');

            data.direction = 'up';
            if (obj.hasClass('down')) {
                data.direction = 'down';
            }
            data.slug = $(this).parent('span').attr('name');
            /**
             * Remove the previous data
             */
            $('.latest_target_prices svg').remove();
            $('#target-price-list').html('');
            /**
             * Pass the information to loader
             */
            loader.sorted(data.slug, data.direction, 0);
        },
        /**
         * Remove content, add to another list
         * Because need to rerun JavaScript for graphs
         */
        change_target_prices_list: function() {

            var content = null;

            list_type = (list_type == 'list') ? 'grid' : 'list'; // ?????
            $('.latest_target_prices svg').remove();
            if ($('#latest-target-price-list').hasClass('list')) {
                $('#latest-target-price-list').removeClass('list');
                $('#latest-target-price-list').addClass('grid');
                /* Reload target prices */
                $('#target-price-list').html('');
                loader.target_prices(0);
            } else {
                $('#latest-target-price-list').removeClass('grid');
                $('#latest-target-price-list').addClass('list');
                /* Reload target prices */
                $('#target-price-list').html('');
                loader.target_prices(0);
            }
        }
    };
})();

$(document).ready(render.document_ready);