/* Target Price */
var tp = (function() {

    var target_prices_list = [];
    var tmp_target_price = {};
    var target_price_sort_info = {};
    var list_type;
    var page_number = Number();
    var loading_target_prices = false;

    var horizontal_slider_top_offset = 0;
    var bottom_of_page = false;
    var search_result = {};

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



    /* Global access functions */
    return {

        append_target_price_list: function(target_price) {
            target_prices_list.push(target_price);
        },

        /* jQuery document ready */
        document_ready: function() {

            $('body').click(in_graph_click);
            $('.in_graph').click(in_graph_click);
            $('.in_graph').hover(in_graph_click);
            $('.in_graph .sear li').click(in_graph_entry_click);
            $('.in_graph .sear li').hover(in_graph_entry_hover);
            $('.in_graph .sear input').keyup(in_graph_search);
            $('.in_graph').mouseleave(in_graph_leave);
            // to clear search proposals
            $('body').click(function() {
                $('.search_res').html('');
            });
            $('.analyse_menu a').click(open_graph);

            $('.inner_buttons a').click(load_target_prices);

            // In analyse page, on document ready, load first property or take from hash!
            var feature = hash_get('feature');
            if (feature == 'target_prices') {
                $('.inner_buttons a.ta').trigger('click');
            } else if (feature.length) {
                $('.analyse_menu div[name=' + feature + '] a').trigger('click');
            } else {
                $('.analyse_menu div:first-child a').trigger('click');
            }

            // long company names moving
            $('.corp_info, .bank .corp').hover(function() {
                var obj = $(this);
                obj.find('.goust').text(obj.find('.text .slid').text());
                var left = Math.min(0, (obj.find('.text').width() - 5 - obj.find('.goust').width()));
                obj.find('.text .slid').animate({
                    'left': left
                }, (left * -15));
            }, function() {
                $(this).find('.text .slid').stop().css({
                    'left': 0
                });
            });

            // s&p500 index popup
            $('.sp500').click(function() {
                var list = $('#popup .list'),
                    elem;
                $.ajax({
                    url: '/tickers/',
                    dataType: 'json'
                }).done(function(data) {
                    $('body').css('overflow', 'hidden');
                    $('#popup').show();
                    $('#popup .list').height($('#popup .content').height() - 68);
                    for (var i = 0; i < data.length; i++) {
                        elem = '<a href="' + data[i].url + '">' + data[i].long_name + ' (' + data[i].name + ')</a>';
                        list.append(elem);
                        if (i % 2) {
                            list.append('<span></span>');
                        }
                    }
                    list.append('<br class="clear" />');
                });
                return false;
            });
            $('#popup .close, #popup .overlay').click(function() {
                $('body').css('overflow', 'auto');
                $('#popup').hide();
                $('#popup .list').html('');
            });

            process_target_prices_blocks();
            binds_for_target_price_list();
            calculate_minavgmax_block();
            load_more_target_prices();
            scroll_style_elements();
            show_compare_graph_buttons();

            if ($('.horizontal_slider').length !== 0) {
                horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
            }
        },


        /* jQuery window scroll */
        window_scroll: function() {
            if ($('.horizontal_slider').length !== 0 && horizontal_slider_top_offset === 0) {
                horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
            }
            // load_more_target_prices();
            scroll_style_elements();
        },

        /** jQuery window resize **/
        window_resize: function() {
            $('#popup .list').height($('#popup .content').height() - 68);
        },


        process_search: function(dom_obj, e) {
            e.preventDefault();
            var key = e.keyCode ? e.keyCode : e.charCode;
            var obj = $('#search_inp');
            var url = '/search/' + obj.val() + '/';

            if (key == 40 || key == 38) {
                process_search_nav(key);
                return;
            }
            if ($(dom_obj).attr('type') == "submit") {
                if ($('#search_inp').attr('href') !== undefined) {
                    location.href = $('#search_inp').attr('href');
                }
                return false;
            }

            if (obj.val().length < 1) {
                $('.search_res').html('');
                return;
            }

            $.ajax({
                url: url,
                dataType: "json"
            }).done(function(resp) {
                var resp_html = '';
                search_result = resp;

                if (resp.tickers.length) {
                    resp_html += '<li class="inf">' +
                        '<a onclick="return tp.process_search_page(\'tickers\')" href="">' +
                        'Companies <span>See all</span></a></li>';
                    for (i = 0; i < resp.tickers.length; i++) {
                        if (i >= 5) {
                            break;
                        }
                        resp_html += '<li class="entry"><a href="' +
                            resp.tickers[i].url + '">' + resp.tickers[i].name +
                            ' (' + resp.tickers[i].ticker + ')</a></li>';
                    }
                }

                if (resp.analytics.length) {
                    resp_html += '<li class="inf">' +
                        '<a onclick="return tp.process_search_page(\'analytics\')" href="">' +
                        'Analysts<span>See all</span></a></li>';
                    for (i = 0; i < resp.analytics.length; i++) {
                        if (i >= 5) {
                            break;
                        }
                        resp_html += '<li class="entry"><a href="' +
                            resp.analytics[i].url + '">' + resp.analytics[i].name + '</a></li>';
                    }
                }

                $('.search_res').html(resp_html);
            });
        },

        process_testing_page_search: function(dom_obj, e) {
            e.preventDefault();
            var key = e.keyCode ? e.keyCode : e.charCode;
            var obj = $('#search_inp');
            var url = '/test_page_search/' + obj.val() + '/';

            if (key == 40 || key == 38) {
                process_search_nav(key);
                return;
            }
            if ($(dom_obj).attr('type') == "submit") {
                if ($('#search_inp').attr('href') !== undefined) {
                    location.href = $('#search_inp').attr('href');
                }
                return false;
            }

            if (obj.val().length < 1) {
                $('.search_res').html('');
                return;
            }

            $.ajax({
                url: url,
                dataType: "json"
            }).done(function(resp) {
                var resp_html = '';
                search_result = resp;

                if (resp.length) {
                    for (i = 0; i < resp.length; i++) {
                        // if(i >= 5) { break; }
                        resp_html += '<li class="entry"><a href="' + resp[i].url + '">' +
                            resp[i].title + '</a></li>';
                    }
                }

                $('.search_res').html(resp_html);
            });
        },

        /**
         * Processing Search
         * 
         * @param  {[type]} type [description]
         * @return {[type]}      [description]
         */
        process_search_page: function(type) {
            var response = '',
                elem, name, search_resul = search_result[type];

            for (var i = 0; i < search_resul.length; i++) {
                name = (type == 'tickers') ? search_resul[i].name +
                    ' (' + search_resul[i].ticker + ')' : search_resul[i].name;
                elem = '<a href="' + search_resul[i].url + '">' + name + '</a>';
                response += elem;
                if (i % 2) {
                    response += '<span></span>';
                }
            }

            $('#content').html('<div class="search_result"></div>');
            $('#content .search_result').append(response);
            $('#content .search_result').append('<br class="clear" />');
            return false;
        },

        /**
         * In Graph Select Active Elements
         * 
         * @return {[type]} [description]
         */
        in_graph_select_active_elements: function() {
            in_graph_select_active_elements();
        },

        /**
         * Updating ticker stock
         * 
         * @param  {[type]} ticker [description]
         * @return {[type]}        [description]
         */
        update_ticker_stock: function(ticker) {
            if ($(".price_detail") !== undefined) {
                var format_text = '';
                $.getJSON('/get_ticker_data/' + ticker + '/', function(data) {
                    /* data.change_direction apraso i kuria puse reikia sukti arrow */
                    $('.price').text(data.last_stock_price);
                    var triangle = (data.change_percent > 0) ? '<i class="up"></i>' : '<i class="down"></i>';
                    format_text = data.change + " (" + triangle + data.change_percent + "%)";
                    $('.price_detail').html(format_text);
                });
            }
        }

    };

    /** 
     * Filtering the minimum value of the feature
     * @param  {[type]} value   [description]
     * @param  {[type]} feature [description]
     * @return {[type]}         [description]
     */
    function filter_minimum_data(value, feature) {
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
    }

    /**
     * Filtering the maximum value of the feature
     * @param  {[type]} value   [description]
     * @param  {[type]} feature [description]
     * @return {[type]}         [description]
     */

    function filter_maximum_data(value, feature) {
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
    }

    /**
     * Filtering the input data to the graphs
     * @param  {[type]} value   [description]
     * @param  {[type]} feature [description]
     * @return {[type]}         [description]
     */

    function filter_graph_data(value, feature) {
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

        value = filter_minimum_data(value, feature);
        value = filter_maximum_data(value, feature);

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
    }

    /**
     * Returning the maximum value of the feature
     * @param  {[type]} feature [description]
     * @return {[type]}         [description]
     */

    function filter_maximum_value(feature) {
        var value = 0;
        switch (feature) {
            case 'accuracy':
                value = filter_maximum_data(10000, feature);
                break;
            case 'profitability':
                value = filter_maximum_data(10000, feature);
                break;
            case 'reach_time':
                value = filter_maximum_data(10000, feature);
        }
        return value;
    }

    /**
     * Generating the pies of data
     * @param  {[type]} id      [description]
     * @param  {[type]} dataset [description]
     * @param  {[type]} posName [description]
     * @return {[type]}         [description]
     */

    function generate_grid_element(id, dataset, posName) {

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
        var max_value = filter_maximum_value(posName);

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
        dataset = filter_graph_data(dataset, posName);

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
    }

    /**
     * Generation of PIE
     * 
     * @param  {[type]} id    [description]
     * @param  {[type]} value [description]
     * @return {[type]}       [description]
     */
    function generate_pie(id, value) {
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
    }

    /**
     * Drawing graph in the target price block
     * @return {[type]} [description]
     */
    function process_target_prices_blocks() {
        for (i = 0; i < target_prices_list.length; i++) {
            if (target_prices_list[i].processed) {
                continue; // What this does?
            }
            target_prices_list[i].processed = true;
            generate_pie(
                target_prices_list[i].hash,
                target_prices_list[i].change);
            generate_grid_element(
                target_prices_list[i].hash,
                target_prices_list[i].accuracy,
                'accuracy');
            generate_grid_element(
                target_prices_list[i].hash,
                target_prices_list[i].profitability,
                'profitability');
            generate_grid_element(
                target_prices_list[i].hash,
                target_prices_list[i].reach_time,
                'reach_time');
        }
    }

    /**
     * [process_search_nav description]
     * @param  {[type]} key [description]
     * @return {[type]}     [description]
     */

    function process_search_nav(key) {

        var list = null;
        var first_time = null;
        var i = 0;

        function _set_active(li_obj) {
            if (li_obj.length) {
                $('.search_res li').removeClass('active');
                li_obj.addClass('active');
                $('#search_inp').val('').val(li_obj.text()).attr('href', li_obj.find('a').attr('href'));
            }
        }

        // nav button down
        if (key == 40) {
            list = $('.search_res li');
            first_time = ($('.search_res li.active').length === 0);
            for (i = 1; i <= list.length; i++) {
                // fist time, no active elements
                if (first_time) {
                    _set_active($('.search_res li:nth-child(2)'));
                    break;
                }
                if (
                    $('.search_res li:nth-child(' + i + ')').hasClass('active') &&
                    $('.search_res li:nth-child(' + (i + 1) + ')').hasClass('inf') === false) {
                    // li nth(i) active and next not have inf class
                    _set_active($('.search_res li:nth-child(' + (i + 1) + ')'));
                    break;
                } else if (
                    $('.search_res li:nth-child(' + i + ')').hasClass('active') &&
                    $('.search_res li:nth-child(' + (i + 1) + ')').hasClass('inf') === true) {
                    // li nth(i) active and next have inf class     
                    _set_active($('.search_res li:nth-child(' + (i + 2) + ')'));
                    break;
                }
            }

        } else if (key == 38) {
            list = $('.search_res li'), first_time = ($('.search_res li.active').length === 0);
            for (i = 1; i <= list.length; i++) {
                // going to input element
                if (i == 2 && $('.search_res li:nth-child(' + i + ')').hasClass('active')) {
                    $('.search_res li').removeClass('active');
                    // cursor to end
                    var tmp_val = $('#search_inp').val();
                    $('#search_inp').val(tmp_val);
                } else if (
                    $('.search_res li:nth-child(' + i + ')').hasClass('active') &&
                    $('.search_res li:nth-child(' + (i - 1) + ')').hasClass('inf') === false) {
                    // li nth(i) active and prev not have inf class 
                    _set_active($('.search_res li:nth-child(' + (i - 1) + ')'));
                    break;
                } else if (
                    $('.search_res li:nth-child(' + i + ')').hasClass('active') &&
                    $('.search_res li:nth-child(' + (i - 1) + ')').hasClass('inf') === true) {
                    // li nth(i) active and prev have inf class
                    _set_active($('.search_res li:nth-child(' + (i - 2) + ')'));
                    break;
                }
            }
        }
    }

    /**
     * Click on property in inner Analyse
     * 
     * @return {[type]} [description]
     */
    function open_graph() {

        obj = $(this);
        if (obj.hasClass('active')) {
            return false;
        }
        var type = obj.parent('div').attr('name');
        var url = obj.attr('href');
        var name = obj.text();
        $('#chart').html('').attr('class', type);
        var graph_fx = eval('graphs.' + type);

        if (typeof(graph_fx) === 'function') {
            graph_fx(url);
            graphs.current_name = name;
            graphs.current_slug = type;
        } else {
            console.log('Graph not ready yet. ' + type);
        }

        $('.analyse_menu a').removeClass('active');
        obj.addClass('active');

        // info box content
        $('.info_box').html(obj.siblings('div').html());
        show_compare_graph_buttons();
        hash_set_feature(type);
        return false; // prevent href (not a good practice)
    }

    /**
     * Setting Active analytic
     */
    function set_active_analytic() {
        // show first target price
        // console.log('Set Active Analytic');
        if ($('#bank li.active').length === 0) {
            var name = hash_get('company');
            if (name.length === 0) {
                name = graphs.get_best_analytic().slug;
                // console.log('best analytic: ' + name);
                hash_set_company(name);
            }
            // console.log('#bank li[name=' + name + ']');
            $('#bank li[name=' + name + ']').addClass('active').removeClass('passive');
            $('.in_graph li[name=' + name + ']').addClass('active');
        }
    }

    /** Get from #hash. opt = "company" or opt = "feature" */
    function hash_get(opt) {
        if (location.hash.length !== 0) {
            var name = location.hash.substr(1);
            var arr = name.split('|', 2);
            if (opt == 'company') {
                return (arr[0] === undefined) ? '' : arr[0];
            } else if (opt == 'feature') {
                return (arr[1] === undefined) ? '' : arr[1];
            }
        } else {
            return '';
        }
    }

    /**
     * [hash_set_company description]
     * @param  {[type]} name [description]
     * @return {[type]}      [description]
     */

    function hash_set_company(name) {
        var feature = hash_get('feature');
        location.hash = '#' + name + '|' + feature;
    }

    /**
     * [hash_set_feature description]
     * @param  {[type]} name [description]
     * @return {[type]}      [description]
     */

    function hash_set_feature(name) {
        var company = hash_get('company');
        location.hash = '#' + company + '|' + name;
    }

    /**
     * [show_compare_graph_buttons description]
     * @return {[type]} [description]
     */

    function show_compare_graph_buttons() {
        var current = $('.analyse_menu a.active').attr('class');
        if (current === undefined) {
            return;
        }
        current = current.replace('active', '').trim();
        $('.analyse_menu div').removeClass('can_compare');

        switch (current) {
            case 'accuracy':
                $('.analyse_menu div[name=proximity]').addClass('can_compare');
                $('.analyse_menu div[name=profitability]').addClass('can_compare');
                $('.analyse_menu div[name=aggressiveness]').addClass('can_compare');
                break;
            case 'proximity':
            case 'profitability':
            case 'aggressiveness':
                $('.analyse_menu div[name=accuracy]').addClass('can_compare');
                break;
        }

        $('.analyse_menu .can_compare > span').removeClass('active');

        $('.analyse_menu .can_compare > span').unbind('click').click(function() {
            $('.analyse_menu .can_compare > span').removeClass('active');
            $(this).addClass('active');
            var slug = $(this).parent('div').attr('name');
            var url = $(this).siblings('a').attr('href');
            var name = $(this).siblings('a').text();
            graphs.compare_graphs(name, slug, url);
        });
    }

    /**
     * [load_target_prices description]
     * @return {[type]} [description]
     */
    function load_target_prices() {

        if ($(this).hasClass('active')) {
            return false;
        }

        var analytic = $('.ta').attr('data-analytic');
        if (analytic === undefined) {
            analytic = null;
        }
        var ticker = $('.ta').attr('data-ticker');
        if (ticker === undefined) {
            ticker = null;
        }

        var url = $(this).attr('href');
        var that = this;
        $('.inner_buttons a').removeClass('active');
        $(this).addClass('active');

        // load targets and stores Analysis html to temp html container
        if (url.length) {
            $('.inner_content').animate({
                'opacity': 0
            }, 50, function() {
                $(this).addClass('hidden');
                $('.inner_target_prices').removeClass('hidden').css('opacity', 0);
                $('.inner_target_prices').animate({
                    'opacity': 1
                }, 100);
                config = {
                    'display': 'grid',
                    'analytic': analytic,
                    'ticker': ticker,
                    'sort': {
                        'slug': null,
                        'direction': null
                    },
                    'page': 0
                };
                loader.target_prices(config);
            });

            hash_set_feature('target_prices');
            // sets Analysis html back from container
        } else {
            $('.inner_target_prices').animate({
                'opacity': 0
            }, 50, function() {
                $(this).addClass('hidden');

                $('.inner_content').removeClass('hidden').css('opacity', 0);
                $('.inner_content').animate({
                    'opacity': 1
                }, 100);
            });
            var feature = $('.analyse_menu a.active');
            if (feature.length === 0) {
                $('.analyse_menu div:first-child a').trigger('click');
                feature = $('.analyse_menu a.active');
            }
            feature = feature.parent('div').attr('name');
            hash_set_feature(feature);
        }
        return false;
    }

    /**
     * Remove content, add to another list
     * Because need to rerun JavaScript for graphs
     */
    function change_target_prices_list() {

        var content = null;

        list_type = (list_type == 'list') ? 'grid' : 'list'; // ?????
        $('.latest_target_prices svg').remove();
        target_prices_list = []; // target prices content will be realoded.
        // set list page
        if ($('.latest_target_prices.hidden').hasClass('list')) {
            $('.latest_target_prices.list').removeClass('hidden');
            $('.latest_target_prices.grid').addClass('hidden');

            content = $('.latest_target_prices.grid').html();
            $('.latest_target_prices.grid').html('');
            $('.latest_target_prices.list').html(content);
            // set grid page
        } else {
            $('.latest_target_prices.grid').removeClass('hidden');
            $('.latest_target_prices.list').addClass('hidden');

            content = $('.latest_target_prices.list').html();
            $('.latest_target_prices.list').html('');
            $('.latest_target_prices.grid').html(content);
        }

        // new content, bind again
        process_target_prices_blocks();
        binds_for_target_price_list();
        load_more_target_prices();
        scroll_style_elements();
    }

    /**
     * [binds_for_target_price_list description]
     * @return {[type]} [description]
     */
    function binds_for_target_price_list() {
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

        $('.latest_target_prices .toggle').unbind('click').click(change_target_prices_list);
        $('.title.list .pre_info span a').unbind('click').click(sort_target_prices);

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
    }

    /**
     * [calculate_minavgmax_block description]
     * @return {[type]} [description]
     */

    function calculate_minavgmax_block() {
        obj = $('.corp_info .avg');
        if (obj.length === 0) {
            return;
        }

        var min = obj.find('.mn i').text();
        var avg = obj.find('.av i').text();
        var max = obj.find('.mx i').text();

        // avg element style is from 55 to 250px left; 50 - 246
        //var percent = 195/(max-min)*(avg-min)+55;
        var percent = 196 / (max - min) * (avg - min) + 50;
        obj.find('.av').css('left', percent);
    }

    /** 
     * [sort_target_prices description]
     * @return {[type]} [description]
     */
    function sort_target_prices() {
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

        $.getJSON('/targets/' + data.slug + '/' + data.direction, function(data) {
            console.log(data);
        });

        // var list_html = $('#target-price-list').clone();
        // $('#target-price-list').html('');
        // // do sort!
        // target_prices_list = get_sorted_target_prices(
        //     target_prices_list,
        //     target_price_sort_info
        // );

        // for (i = 0; i < target_prices_list.length; i++) {
        //     $('#target-price-list').append(
        //         list_html.find('#' + target_prices_list[i].hash)
        //     );
        // }
        // binds_for_target_price_list();
    }

    /**
     * Returning sorted target prices
     *
     * List format
     *
     * - accuracy: @string
     * - change: @string
     * - hash: @string
     * - name: @string
     * - processed: @boolean
     * - profitability: @string
     * - reach_time: @string
     * 
     * @param  {[type]} list      [description]
     * @param  {[type]} sort_info [description]
     * @return {[type]}           [description]
     */

    // function get_sorted_target_prices(list, sort_info) {
    //     var new_list = [];
    //     var url = '/targets/'+ sort_info.slug +'/' + sort_info.direction;
    //     $.getJSON(url , function(data) {
    //         data.each(function(element) {
    //             new_list.push({
    //                 'hash': element.hash,
    //                 'price': element.price
    //             });
    //         });
    //         return new_list;
    //     });
    //     if (sort_info.direction == 'up') {
    //         new_list.sort(function(a, b) {
    //             return b[sort_info.slug] - a[sort_info.slug];
    //         });
    //     } else {
    //         new_list.sort(function(a, b) {
    //             return a[sort_info.slug] - b[sort_info.slug];
    //         });
    //     }
    //     return new_list;
    // }

    /**
     * [in_graph_click description]
     * @return {[type]} [description]
     */

    function in_graph_click() {
        console.log('In graph click');
        var obj = $(this);

        if ($('.in_graph').hasClass('tmp')) {
            $('.in_graph').removeClass('tmp');
            return;
        }

        // Adding something ??
        if (obj.parents().length > 2) {
            obj.addClass('tmp');
            obj.addClass('active');
            $(".in_graph .sear ul").niceScroll({
                'cursorborder': '0px',
                'cursorcolor': '#cdcdcd',
                'cursorwidth': '6px'
            });
            // nice scroll
            $('#ascrail2000, #ascrail2000-hr').css('visibility', 'visible');
        } else {
            $('.in_graph').removeClass('active');
            // nice scroll
            $('#ascrail2000, #ascrail2000-hr').css('visibility', 'hidden');
        }
    }

    /**
     * Hiding the in_graph menu
     * 
     * @return {[type]} [description]
     */
    function in_graph_leave() {
        $('.in_graph').removeClass('active');
        // Nice scroll
        $('#ascrail2000, #ascrail2000-hr').css('visibility', 'hidden');
    }

    /**
     * [in_graph_entry_click description]
     * @return {[type]} [description]
     */

    function in_graph_entry_click() {
        var obj = $(this);
        var name = obj.attr('name');
        var svg_element = $('#chart svg [name=' + name + ']');

        if (obj.hasClass('active')) {
            obj.removeClass('active');
            svg_element.attr('fill', svg_element.attr('origin_fill')).attr('selectd', 0);
        } else {
            obj.addClass('active');
            svg_element.attr('fill', '#e95201').attr('selectd', 1);
        }
    }

    /**
     * [in_graph_entry_hover description]
     * @param  {[type]} e [description]
     * @return {[type]}   [description]
     */

    function in_graph_entry_hover(e) {
        var obj = $(this);
        var name = obj.attr('name');
        var svg_element = $('#chart svg [name=' + name + ']');
        if (e.type == 'mouseenter') {
            svg_element.attr('fill', '#e95201').css('opacity', 0.7);
            graphs.topbar_show(obj.attr('name'));

        } else if (e.type == 'mouseleave' && obj.hasClass('active')) {
            svg_element.css('opacity', 1);

        } else if (e.type == 'mouseleave') {
            svg_element.attr('fill', svg_element.attr('origin_fill')).css('opacity', 1);
        }
    }

    /**
     * [in_graph_get_active_elements description]
     * @return {[type]} [description]
     */

    function in_graph_get_active_elements() {
        var list = $('.in_graph .sear li');
        var obj, name, active_elements = [];

        list.each(function() {
            obj = $(this);
            name = obj.attr('name');
            if (obj.hasClass('active')) {
                active_elements.push(name);
            }
        });
        return [];
        //return active_elements;
    }

    /**
     * [in_graph_select_active_elements description]
     * @return {[type]} [description]
     */

    function in_graph_select_active_elements() {
        set_active_analytic(); // for first time. if any

        var list = $('.in_graph .sear li');
        var obj, name, svg_element;

        list.each(function() {
            obj = $(this);
            name = obj.attr('name');
            svg_element = $('#chart svg [name=' + name + ']');

            if (obj.hasClass('active')) {
                svg_element.attr('fill', '#e95201').attr('selectd', 1);
            }
        });
    }

    /**
     * [in_graph_search description]
     * @return {[type]} [description]
     */

    function in_graph_search() {
        var list = $('.in_graph ul li');
        var search_for = new RegExp($(this).val(), 'i');

        list.each(function() {
            var item = $(this);
            if (item.text().search(search_for) == -1) {
                item.hide();
            } else {
                item.show();
            }
        });
    }

    /**
     * Scroll
     ***/

    function scroll_style_elements() {

        var card_group_position = 0;
        var card_group_height = 0;
        var window_scroll = $(window).scrollTop();

        if (window_scroll > horizontal_slider_top_offset) {

            if ($('.horizontal_slider').hasClass('absolute')) {
                $('.horizontal_slider').removeClass('absolute');
            }
            if (!$('.horizontal_slider').hasClass('fixed')) {
                $('.horizontal_slider').addClass('fixed');
            }

        } else {
            if ($('.horizontal_slider').hasClass('absolute')) {
                $('.horizontal_slider').removeClass('fixed');
            }
            if (!$('.horizontal_slider').hasClass('absolute')) {
                $('.horizontal_slider').addClass('absolute');
            }
        }

        // set target prices Date (html element on the right)
        var obj, exit = false;
        $('.target_price_list li').each(function(index, entry) {
            if (exit) {
                return;
            }
            obj = $(entry);
            if (
                obj.offset().top <= window_scroll + 50 &&
                obj.offset().top + obj.outerHeight() +
                parseInt(obj.css('margin-bottom'), 10) >= window_scroll + 50) {
                $('.now').text(obj.attr('name'));
                exit = true;
            }

        });

    }

    /**
     * [load_more_target_prices description]
     * @return {[type]} [description]
     */

    function load_more_target_prices() {
        // don't use in inner, analyse page
        if ($('.inner_target_prices').length) {
            return false;
        }

        /* Give it a bigger offset, for better experience */

        var last_offset = 0;

        if ($('.target_price_list > li:nth-last-of-type(1)').offset() !== undefined) {
            last_offset = $('.target_price_list > li:nth-last-of-type(1)').offset().top;
        } else {
            return false;
        }

        if (
            $(window).scrollTop() + $(window).height() >= last_offset + 310 &&
            bottom_of_page === false &&
            loading_target_prices === false) {
            page_number += 1;
            loading_target_prices = true;

            /* Make a query */
            _url = "/page/" + page_number + "/";
            // TODO: set target price sorting from {target_price_sort_info} variable
            $.ajax({
                url: _url,
                context: $("#target-price-list")
            }).done(function(data) {
                $("#target-price-list").append(data);
                loading_target_prices = false;
                // if one loaded page is not enough, bind and process if no more to load.
                if (load_more_target_prices() === false) {
                    process_target_prices_blocks();
                    binds_for_target_price_list();
                }
            }).error(function() {
                bottom_of_page = true;
            });
            return true; // loaded more target prices
        } else {
            return false; // not loaded, enough
        }
    }


})();


/* Bind main functions execution */
$(document).ready(tp.document_ready);
$(window).scroll(tp.window_scroll);
$(window).resize(tp.window_resize);

/* Internet Explorer save console.log() */
// Why?
// if (typeof(console)=="undefined"){var console={log:function(){}};}