/**
 * Graph drawing library for Target Price project
 *
 * Usage:
 * graphs.method(url)
 * - method: accuracy/proximity/...
 * - url: url from where to fetch data
 */
var graphs = (function () {

    var _url = '';
    var _element_id = "chart";
    var _data = [];
    var full_data = []; // refactor, real, full data variable.
    var current_name;
    var current_slug;
    var host = "";
    var active_topbar = "";
    var best_analytic = {
        value: 0
    };

    var _number_of_graphs = 0;

    /* Clear the current graph (in case of `active` graph update) */
    d3.selectAll("#" + _element_id + " svg").remove();

    return {
        set_url: function (url) {
            /**
             * Setting url
             * (not sure if needed anymore)
             */
            _url = url;
        },
        get_best_analytic: function () {
            return best_analytic;
        },

        topbar_show: function (slug) {
            if (active_topbar == slug) {
                return;
            }

            active_topbar = slug;
            graphs.topbar_hide();
            d3.select(".bank li[name='" + slug + "']").attr('class', 'active').style('background-color', '#FAFAFA').transition().duration(300).style('background-color', '#fff');
        },

        topbar_hide: function () {
            d3.selectAll(".bank li[class='active']").attr('class', 'passive');
        },

        tooltip_show: function (top, left, text) {
            d3.selectAll("#chart div").remove();
            d3.select("#chart")
                .append('div')
                .attr('class', 'bar_tooltip')
                .text(text)
                .style("left", left + "px")
                .style("top", top + "px")
                .style('font-size', function () {
                return (text.length >= 5) ? '11px' : '12px';
            })
                .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1);
        },

        on_mouseout: function () {
            if (d3.select(this).attr('selectd') == 0) {
                d3.select(this).attr("fill", d3.select(this).attr('origin_fill'));
            }
            d3.select(this).style('opacity', 1);
        },

        on_click: function(){
            var name = d3.select(this).attr('name');
            $('.in_graph .sear li[name='+name+']').trigger('click');
        },

        populate: function (json) {
            var tmp_obj, f_data = [];

            for (i = 0; i < json.length; i++) {
                tmp_obj = {};
                // TODO: why values come negative?
                // set values max 100, min 0
                tmp_obj.value = Math.max(0, json[i].value);
                tmp_obj.value = Math.min(100, tmp_obj.value);

                // analytics (banks) in graph
                if (json[i].ticker__slug === undefined) {
                    tmp_obj.name = json[i].analytic__name;
                    tmp_obj.slug = json[i].analytic__slug;
                    tmp_obj.type = 'analytic';

                    // ticker (company) in graph
                } else {
                    tmp_obj.name = json[i].ticker__name;
                    tmp_obj.slug = json[i].ticker__slug;
                    tmp_obj.type = 'ticker';
                }

                f_data.push(tmp_obj);

                if (tmp_obj.value > best_analytic.value) {
                    best_analytic = tmp_obj;
                }
            }

            return f_data;
        },

        get__data: function (d) {
            var new_d = [];
            for (i = 0; i < d.length; i++) {
                new_d.push(d[i].value);
            }
            return new_d;
        },

        /* Reorder full_data array, move active element to begin of array */
        reorder_UNUSED: function(order_elem_name){
            var elem, to_end = true;
            switch(graphs.current_slug){
                case 'profitability':
                case 'impact_to_market':
                case 'accuracy':
                to_end = false;
                break;
            }

            for (var i = 0 ; i < full_data.length; i++) {
                if(full_data[i].slug == order_elem_name){
                    if(to_end === true){
                        full_data.push(full_data[i]);
                        full_data.splice(i, 1);
                    }else{
                        full_data.unshift(full_data[i]);
                        full_data.splice(i+1, 1);
                    }
                    break;
                }
            }
            return;
        },
        draw_reordered_UNUSED: function(){

            d3.selectAll("#" + _element_id + " svg").remove();
            _data = graphs.get__data(full_data);
            var graph_fx = eval('graphs.draw_'+graphs.current_slug);
            graph_fx(); // run
        },

        aggressiveness: function (url) {
            /**
             * Aggressiveness request
             */
            d3.json(host + url, function (error, json) {
                if (!error) {

                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_aggressiveness();
                    tp.in_graph_select_active_elements();

                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        profitability: function (url) {
            /**
             * Profitability request
             */
            d3.json(host + url, function (error, json) {
                if (!error) {

                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return b.value - a.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_profitability();
                    tp.in_graph_select_active_elements();

                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        accuracy: function (url, phase) {
            /**
             * Accuracy request
             */
            d3.json(host + url, function (error, json) {
                if (!error) {
                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return b.value - a.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_accuracy();
                    tp.in_graph_select_active_elements();
                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        reach_time: function (url) {
            /**
             * Reach time request
             */
            d3.json(host + url, function (error, json) {
                if (!error) {
                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return b.value - a.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_reach_time();
                    tp.in_graph_select_active_elements();

                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        impact_to_market: function (url) {
            /**
             * Impact to stock request
             */
            d3.json(host + url, function (error, json) {
                if (!error) {

                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return b.value - a.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_impact_to_market();
                    tp.in_graph_select_active_elements();

                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        proximity: function (url) {
            /**
             * Proximity graph request
             */
            d3.json(host + url, function (error, json) {
                /* XHR check */
                if (!error) {
                    /* Populate the data */
                    full_data = graphs.populate(json);
                    full_data.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    _data = graphs.get__data(full_data);
                    graphs.draw_proximity();
                    tp.in_graph_select_active_elements();
                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
            return graphs;
        },

        draw_proximity: function () {
            /**
             * Method to draw proximity graphic
             */

            /* Calculate constants */
            var w = $("#" + _element_id).width() - 20,
                h = $("#" + _element_id).height() - 30,
                r = Math.min(w, h) / 20,
                rhw = Math.min(w, h) / 2.25,
                color = d3.scale.category20c();

            var sun = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);
            pi = Math.PI;

            // fill with bulk data to have lost of lines, circle r=0 for false value
            var lines = 50,
                data_proximity = [],
                full_data_proximity = [],
                n = 0,
                j = 0,
                space;
            if (lines > _data.length) {
                for (i = 0; i < lines; i++) {
                    space = Math.floor((lines - i - 1) / (_data.length - j));
                    if (space <= n) {
                        data_proximity.push(_data[j]);
                        full_data_proximity.push(full_data[j]);
                        j++;
                        n = 0;
                    } else {
                        data_proximity.push(false);
                        full_data_proximity.push({});
                        n++;
                    }
                }
            } else {
                data_proximity = $.extend([], _data);
                full_data_proximity = $.extend([], full_data);
            }

            angle_scale = d3.scale.linear().domain([0, data_proximity.length]).range([0, 2 * pi]);

            angle_arc = d3.svg.arc()
                .innerRadius(r)
                .outerRadius(function (d, i) {
                return rhw + r;
            })
                .startAngle(function (d, i) {
                return angle_scale(i) + pi / 2;
            })
                .endAngle(function (d, i) {
                return angle_scale(i) + pi / 2;
            });

            sun.selectAll('.stripes')
                .data(data_proximity).enter()
                .append('svg:path')
                .attr("d", function (d, i) {
                return angle_arc(d, i);
            })
                .attr('stroke-width', 0.1)
                .attr('fill', 'none')
                .attr("stroke", "grey")
                .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

            sun.selectAll('.stripes')
                .data(data_proximity).enter()
                .append('svg:circle')
                .attr('cx', function (d, i) {
                return (d / 100 * rhw + r) * Math.cos(angle_scale(i));
            })
                .attr('cy', function (d, i) {
                return (d / 100 * rhw + r) * Math.sin(angle_scale(i));
            })
                .attr('r', function (d, i) {
                if (d === false) {
                    return 0;
                } else {
                    return 6;
                }
            })
                .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")")
                .attr('fill', '#c0be81')
                .attr('origin_fill', '#c0be81')
                .attr('selectd', 0)
                .attr('txt', function (d, i) {
                return data_proximity[i] + ' %';
            })
                .attr('name', function (d, i) {
                return full_data_proximity[i].slug;
            })
                .on('mouseover', function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var top = h / 2 + parseFloat(d3.select(this).attr('cy')) - 37;
                var left = w / 2 + parseFloat(d3.select(this).attr('cx')) - 23;
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data_proximity[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click);

            sun.append('circle')
                .style('stroke', 'grey')
                .style('fill', 'none')
                .attr('stroke-width', 0.5)
                .attr('cx', w / 2)
                .attr('cy', h / 2)
                .attr('r', r);

            return graphs;
        },

        draw_aggressiveness: function () {
            /*
             * Method to draw aggressiveness.
             */

            var sun_data = [0, 20, 40, 60, 80, 100];
            pi = Math.PI;
            rect_w = 20;
            angle_scale = d3.scale.linear().domain([0, _data.length]).range([0, 2 * pi]);

            var w = $("#" + _element_id).width() - 20,
                h = $("#" + _element_id).height() - 40,
                r = Math.min(w, h) / 30,
                rhw = Math.min(w, h) / 2.2,
                color = d3.scale.category20c();

            var sun = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            sun.selectAll("#" + _element_id)
                .data(sun_data).enter().append('circle')
                .style('stroke', '#ece7e3')
                .style('fill', 'none')
                .attr('cx', w / 2)
                .attr('cy', h / 2)
                .attr('r', function (d, i) {
                return (d / 100 * rhw + r);
            });

            sun.selectAll("#" + _element_id).data(sun_data).enter()
                .append("svg:rect")
                .attr("width", function (d) {
                return d.toString().length * 10;
            })
                .attr("height", 20)
                .attr("fill", "#FFFBF8")
                .attr("y", function (d) {
                return -(d / 100 * rhw + r) - 10;
            })
                .attr("x", function (d) {
                return -d.toString().length / 2 * 10;
            })
                .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

            sun.selectAll("#" + _element_id).data(sun_data).enter()
                .append("svg:text")
                .style("text-anchor", "middle")
                .style("width", "10px")
                .style("height", "10px")
                .style("font-size", "10px")
                .style("fill", "#dfc8b6")
                .attr("dy", function (d, i) {
                return -(d / 100 * rhw + r) + 5;
            })
                .text(function (d) {
                return d;
            })
                .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

            sun.selectAll('.stripes')
                .data(_data).enter()
                .append('svg:circle')
                .attr('cx', function (d, i) {
                return (d / 100 * rhw + r) * Math.cos(angle_scale(i));
            })
                .attr('cy', function (d, i) {
                return (d / 100 * rhw + r) * Math.sin(angle_scale(i));
            })
                .attr('r', 6)
                .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")")
                .attr('fill', '#71859e')
                .attr('origin_fill', '#71859e')
                .attr('selectd', 0)
                .attr('txt', function (d, i) {
                return _data[i] + ' %';
            })
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })
                .on('mouseover', function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var top = h / 2 + parseFloat(d3.select(this).attr('cy')) - 34;
                var left = w / 2 + parseFloat(d3.select(this).attr('cx')) - 22.5;
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click);
            return graphs;
        },

        draw_profitability: function () {
            /*
             * Draw profitability graph
             */

            var linear_data = [0, 20, 40, 60, 80, 100];

            var w = $("#" + _element_id).width() - 20,
                h = $("#" + _element_id).height() - 20,
                rhw = h / 106,
                translate_w = w / 16,
                translate = "translate(" + translate_w / 3 * 2 + "," + h + ")";

            var linear = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            linear.selectAll("#" + _element_id).data(linear_data).enter()
                .append("svg:rect")
                .attr('fill', "#e7e2de")
                .attr('width', function () {
                return w - translate_w;
            })
                .attr('height', 0.5)
                .attr("x", 10)
                .attr("y", function (d) {
                return d === 0 ? -10 : -d * rhw - 10;
            })
                .attr("transform", translate);

            linear.selectAll("#" + _element_id).data(linear_data).enter()
                .append("svg:text")
                .style("text-anchor", "end")
                .style("width", "10px")
                .style("height", "10px")
                .style("font-size", "10px")
                .style("fill", "#dec7b5")
                .attr("dy", function (d, i) {
                return d === 0 ? -5 : -d * rhw - 5;
            })
                .attr("dx", function (d, i) {
                return 5;
            })
                .text(function (d) {
                return d;
            })
                .attr("transform", translate);

            linear.selectAll("#" + _element_id).data(_data).enter()
                .append("svg:rect")
                .attr("fill", "#dfc8b6")
                .attr('width', 0.7)
                .attr('height', function (d, i) {
                return d * rhw;
            })
                .attr('y', function (d, i) {
                return -d * rhw - 10;
            })
                .attr('x', function (d, i) {
                return (i + 1) * (w - translate_w) / (_data.length + 1);
            })
                .attr("transform", translate);

            linear.selectAll('#' + _element_id).data(_data).enter()
                .append('svg:circle')
                .attr('cx', function (d, i) {
                return (i + 1) * (w - translate_w) / (_data.length + 1);
            })
                .attr('cy', function (d, i) {
                return -d * rhw - 10;
            })
                .attr('r', 6)
                .attr('fill', '#ac8dc6')
                .attr('origin_fill', '#ac8dc6')
                .attr('selectd', 0)
                .attr('txt', function (d, i) {
                return _data[i] + ' %';
            })
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })

            .on('mouseover', function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var top = h + parseFloat(d3.select(this).attr('cy')) - 37;
                var left = translate_w / 3 * 2 + parseFloat(d3.select(this).attr('cx')) - 23;
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click)
                .attr("transform", translate);
            return graphs;
        },

        draw_accuracy: function () {
            /**
             * Method to draw accuracy
             */

            pi = Math.PI;
            phase = 0;
            var sun_data = [0, 20, 40, 60, 80, 100];

            var w = $("#" + _element_id).width() - 20,
                h = $("#" + _element_id).height(),
                r = Math.min(w, h) / 5,
                rhw = Math.min(w, h) / 1.56,
                color = d3.scale.category20c();

            number_of_data_for_full_graph = 8;

            line_width = w / 7;
            rect_w = 20;

            if (_data.length <= number_of_data_for_full_graph) {
                angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi / 2, pi / 2]);
            } else {
                angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi / 2 - phase, pi - phase]);
                _angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi / 2 - phase, pi - phase]);
            }

            line_angle_scale = d3.scale.linear().domain([-w / 14, w / 14]).range([0, 1 / 2 * pi]);

            var dragCircle = d3.behavior.drag()
            .on('dragstart', function () {
                d3.event.sourceEvent.stopPropagation();
            })
            .on('drag', function (d, i) {
                d.cx = parseInt(d3.select(this).attr('cx'));
                d.cx += d3.event.dx;

                d.cx = Math.min(d.cx, w / 14);
                d.cx = Math.max(d.cx, -w / 14);
    
                d3.select(this).attr('cx', d.cx);
                d3.select(this).attr("transform", "translate(" + d.cx + ", 0)");
                phase = line_angle_scale(d.cx);
                angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi / 2 - phase, pi - phase]);
                sun.selectAll("path.data")
                    .data(_data)
                    .attr("d", data_arc);
            });


            $('.in_graph .sear li').click(function(e){
                return; // disable till better implementation.

                /* Scroll to selected circle element */
                if ($(this).hasClass('active') === false || e.isTrigger === true) {
                    return;
                }
                var name = $(this).attr('name');
                var obj = $('#chart svg path[name='+name+']');
                var nr = parseInt(obj.attr('enumerator'), 10);

                /* TODO: make it work better. */
                var invert_line_angle_scale = d3.scale.linear().domain([0, _data.length-1]).range([-w / 14, w / 14]);
                d = { cx: invert_line_angle_scale(nr) };

                d3.select('.scroller')
                    .transition().duration(700).ease('linear')
                    .attr('cx', d.cx).attr("transform", "translate(" + d.cx + ", 0)");

                phase = line_angle_scale(d.cx);
                angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi / 2 - phase, pi - phase]);
                sun.selectAll("path.data")
                    .data(_data)
                    .transition().duration(750).ease('linear')
                    .attr("d", data_arc);
            });

            var angle_arc = d3.svg.arc()
                .innerRadius(function (d, i) {
                return d / 100 * rhw + r;
                //return r;
            })
                .outerRadius(function (d, i) {
                return d / 100 * rhw + r;
            })
                .startAngle(function (d, i) {
                return -pi / 2;
            })
                .endAngle(function (d, i) {
                return pi / 2;
            });

            var calculate_start_angle = function (i, angle_scale) {
                start_angle = angle_scale(i);
                if (start_angle <= -pi && start_angle > -3 / 2 * pi) {
                    start_angle = -3 / 2 * pi;
                }
                if (start_angle >= -pi && start_angle <= -pi / 2) {
                    start_angle = -pi / 2;
                }
                if (start_angle >= pi && start_angle <= 3 / 2 * pi) {
                    start_angle = 3 / 2 * pi;
                }
                if (start_angle <= pi && start_angle >= pi / 2) {
                    start_angle = pi / 2;
                }
                return start_angle;
            };

            var calculate_end_angle = function (i, angle_scale) {
                end_angle = angle_scale(i + 1);
                start_angle = calculate_start_angle(i, angle_scale);

                if (end_angle <= -pi && end_angle > -3 / 2 * pi) {
                    end_angle = -3 / 2 * pi;
                }
                if (end_angle >= -pi && end_angle <= -pi / 2) {
                    end_angle = -pi / 2;
                }
                if (end_angle >= pi && end_angle <= 3 / 2 * pi) {
                    end_angle = 3 / 2 * pi;
                }
                if (end_angle <= pi && end_angle >= pi / 2) {
                    end_angle = pi / 2;
                }

                if (end_angle - start_angle < 0) {
                    end_angle = start_angle;
                }

                if (end_angle - start_angle == pi) {
                    end_angle = start_angle;
                }
                return end_angle;
            };

            var data_arc = d3.svg.arc()
                .innerRadius(function (d, i) {
                return r;
            })
                .startAngle(function (d, i) {
                start_angle = calculate_start_angle(i, angle_scale);
                return start_angle;
            })
                .endAngle(function (d, i) {
                end_angle = calculate_end_angle(i, angle_scale);
                return end_angle;
            })
                .outerRadius(function (d, i) {
                radius = r;
                if (Math.abs(calculate_start_angle(i, angle_scale) - calculate_end_angle(i, angle_scale)) !== 0) {
                    radius = d / 100 * rhw + r;
                }
                return radius;
            });

            var sun = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            if (_data.length > number_of_data_for_full_graph) {

                sun.append('svg:rect')
                    .attr("x", w / 2 - w / 14 - 6)
                    .attr("y", h - h / 32)
                    .attr('width', (w / 2 + w / 14) - (w / 2 - w / 14) + 10)
                    .attr("height", 5)
                    .attr('rx', 4)
                    .attr('ry', 4)
                    .attr('fill', "#ccb5a5")
                    .attr('stroke', "#baa08b");

                var path = sun.append("g").attr("transform", "translate(" + (w / 2 -6) + "," + (h - h / 32 * 2) + ")");

                path.append('path')
                    .data([{
                        cx: -w / 14
                    }
                ])
                    .attr('d', 'm 0.0389418,0.0432822 9.9610575,0 -0.06029,5.0188999 0,5.2846009 -5.2480518,4.6774 -0.01414,-0.038 L 0,10.005182 0.049611,0.0241822')
                    .attr('fill', '#df5401')
                    .call(dragCircle)
                    .attr('class', 'scroller')
                    .attr('cx', function (d) {
                    return d.cx;
                })
                    .attr("transform", "translate(" + (-w / 14) + ", 0)")
                    .attr('style', 'cursor:pointer');

            }
            sun.selectAll('#' + _element_id)
                .data(sun_data).enter()
                .append('svg:path')
                .attr("d", function(d, i){ if(i==0){d = -0.5;} return angle_arc(d,i) } )
                .attr('stroke-width', 1)
                .attr("stroke", "#f1ebe7")
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            sun.selectAll("#" + _element_id)
                .data(_data).enter()
                .append('svg:path')
                .attr('class', 'data')
                .attr("d", data_arc)
                .attr('stroke', '#FEFAF7')
                .attr('stroke-width', 1)
                .attr('fill', '#8dc6b3')
                .attr('origin_fill', '#8dc6b3')
                .attr('selectd', 0)
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })
                .on("mouseover", function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var angle = (angle_scale(parseFloat(d3.select(this).attr('enumerator'))) + angle_scale(parseFloat(d3.select(this).attr('enumerator')) + 1)) / 2 - pi;
                var radius = parseFloat(d3.select(this).attr('txt'));
                var top = (h - h / 8) + Math.cos(angle) * (radius * rhw / 100 + r);
                var left = w / 2 - Math.sin(angle) * (radius * rhw / 110 + r);
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click)
                .attr('txt', function (d) {
                return d + "%";
            })
                .attr('enumerator', function (d, i) {
                return i;
            })
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            sun.selectAll('#' + _element_id)
                .data(sun_data).enter()
                .append('svg:rect')
                .attr('width', 0.1)
                .attr('height', 6)
                .attr('fill', '#ded1c6')
                .attr('y', 0)
                .attr('x', function (d, i) {
                    if (i===0) {
                        d = -0.5;
                    }
                    return d / 100 * rhw + r;
            })
                .attr("stroke", "#ded1c6")
                .attr('stroke-width', 0.5)
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            sun.selectAll("#" + _element_id)
                .data(sun_data).enter()
                .append("svg:text")
                .style("text-anchor", "left")
                .style("width", "10px")
                .style("height", "10px")
                .style("font-size", "10px")
                .style("fill", "#ded1c6")
                .attr("dy", 18)
                .attr("dx", function (d, i) {
                    if (i===0) {
                        d = 1.7;
                    }
                    return d / 100 * rhw + r - (-0.8 + String(d).length*3.3);
                })
                .text(function (d) {
                return d;
            })
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            sun.selectAll('#' + _element_id)
                .data([1, -1]).enter().append("svg:line")
                .attr('x1', function(d,i){ return (1 / 100 * rhw + r - 4) * d; } )
                .attr('x2', function(d,i){ return (rhw + r) * d; })
                .attr('y1', 0)
                .attr('y2', 0)
                .attr('stroke', '#f1ebe7')
                .attr('stroke-width', 1)
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            return graphs;
        },




        draw_reach_time: function () {
            /**
             ** Method to draw reach time
             ***/
            var linear_data = [0, 20, 40, 60, 80, 100];

            var w = $("#" + _element_id).width(),
                h = $("#" + _element_id).height(),
                rhw = w / 109,
                translate_w = w / 16,
                graph_height = h - 15,
                translate = "translate(" + translate_w / 3 * 2 + "," + h + ")";

            var linear = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            linear.selectAll("#" + _element_id).data(linear_data).enter()
                .append("svg:rect")
                .attr('fill', "#f4ede7")
                .attr('height', function () {
                return graph_height - 25;
            })
                .attr('width', 1)
                .attr("x", function (d, i) {
                return d * rhw;
            })
                .attr("y", -graph_height)
                .attr("transform", translate);

            linear.selectAll("#" + _element_id).data(linear_data).enter()
                .append("svg:text")
                .attr("text-anchor", "left")
                .attr("width", "10px")
                .attr("height", "10px")
                .style("font-size", "10px")
                .style("fill", "#dec7b5")
                .attr("dy", -10)
                .attr("dx", function (d, i) {
                return d * rhw - (-0.7 + new String(d).length*2.9); // can't center with text-anchor, because of firefox and opera bug 
            })
                .text(function (d) {
                return d;
            })
                .attr("transform", translate);

            linear.selectAll("#" + _element_id).data(_data).enter()
                .append("svg:rect")
                .attr("fill", "#e7d9cd")
                .attr('width', function (d, i) {
                return d * rhw;
            })
                .attr('height', 1)
                .attr('y', function (d, i) {
                return -graph_height / (_data.length + 1) * (i + 1);
            })
                .attr('x', 0)
                .attr('txt', function (d, i) {
                return d + ' %';
            })
                .attr("transform", translate);

            linear.selectAll('#' + _element_id).data(_data).enter()
                .append('svg:circle')
                .attr('cx', function (d, i) {
                return d * rhw;
            })
                .attr('cy', function (d, i) {
                return -graph_height / (_data.length + 1) * (i + 1);
            })
                .attr('r', 6)
                .attr('fill', '#91bcc5')
                .attr('origin_fill', '#91bcc5')
                .attr('selectd', 0)
                .attr('txt', function (d, i) {
                return _data[i] + ' %';
            })
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })
                .on('mouseover', function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var top = h + parseFloat(d3.select(this).attr('cy')) - 37;
                var left = translate_w / 3 * 2 + parseFloat(d3.select(this).attr('cx')) - 23;
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click)
                .attr("transform", translate);

            return graphs;
        },

        draw_impact_to_market: function () {
            /**
             * Method to draw impact to market
             */
            pi = Math.PI;
            phase = 0;
            var sun_data = [0, 0, 100];
            var w = $("#" + _element_id).width() - 0,
                h = $("#" + _element_id).height() - 120,
                r = Math.min(w, h) / 2.2,
                rhw = Math.min(w, h) / 2.4,
                color = d3.scale.category20c();

            number_of_data_for_full_graph = 8;

            line_width = w / 7;
            rect_w = 20;

            if (_data.length <= number_of_data_for_full_graph) {
                angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi / 2, pi / 2]);
            } else {
                angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi / 2 - phase, pi - phase]);
            }

            line_angle_scale = d3.scale.linear().domain([-w / 14, w / 14]).range([0, 1 / 2 * pi]);

            var dragCircle = d3.behavior.drag()
            .on('dragstart', function () {
                d3.event.sourceEvent.stopPropagation();
            })
            .on('drag', function (d, i) {
                d.cx = parseInt(d3.select(this).attr('cx'));
                d.cx += d3.event.dx;

                d.cx = Math.min(d.cx, w / 14);
                d.cx = Math.max(d.cx, -w / 14);

                d3.select(this).attr('cx', d.cx).attr('transform', 'translate(' + d.cx + ',0)');

                phase = line_angle_scale(d.cx);
                angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi / 2 - phase, pi - phase]);
                sun.selectAll("path.data")
                    .data(_data)
                    .attr("d", data_arc);
                sun.selectAll("path.data2")
                    .data(_data)
                    .attr("d", data_arc2);

                console.log('scroll', d.cx);
            });

            $('.in_graph .sear li').click(function(e){
                /* Scroll to selected circle element */

                if($(this).hasClass('active') == false || e.isTrigger == true) { return; }
                var name = $(this).attr('name');
                var obj = $('#chart svg path[name='+name+']');
                var nr = parseInt(obj.attr('enumerator'));
                
                /* TODO: make it work better. */
                var invert_line_angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-w / 14, w / 14]);
                var subtotal = 0;
                for (var i = 0; i < _data.length ; i++) {
                    if(i >= nr) { break; }
                    subtotal += _data[i];
                }
                if(nr >= _data.length -2) { subtotal = d3.sum(_data); }

                d = { cx: invert_line_angle_scale(subtotal) };

                d3.select('.scroller')
                    .transition().duration(700).ease('linear')
                    .attr('cx', d.cx).attr("transform", "translate(" + d.cx + ", 0)");

                phase = line_angle_scale(d.cx);
                angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi / 2 - phase, pi - phase]);
                sun.selectAll("path.data")
                    .data(_data)
                    .transition().duration(700).ease('linear')
                    .attr("d", data_arc);
                sun.selectAll("path.data2")
                    .data(_data)
                    .transition().duration(700).ease('linear')
                    .attr("d", data_arc2);
            });

            var calculate_start_angle = function (i, angle_scale) {
                angle_sum = 0;

                for (var k = 0; i - 1 >= k; ++k) {
                    angle_sum += _data[k];
                }

                start_angle = angle_scale(angle_sum);

                if (start_angle <= -pi && start_angle > -3 / 2 * pi) {
                    start_angle = -3 / 2 * pi;
                }
                if (start_angle >= -pi && start_angle <= -pi / 2) {
                    start_angle = -pi / 2;
                }
                if (start_angle >= pi && start_angle <= 3 / 2 * pi) {
                    start_angle = 3 / 2 * pi;
                }
                if (start_angle <= pi && start_angle >= pi / 2) {
                    start_angle = pi / 2;
                }
                return start_angle;
            };

            var calculate_end_angle = function (i, angle_scale) {
                angle_sum = 0;

                for (var k = 0; i >= k; ++k) {
                    angle_sum += _data[k];
                }

                //console.log("End angle sum:", angle_sum)

                end_angle = angle_scale(angle_sum);
                start_angle = calculate_start_angle(i, angle_scale);

                if (end_angle <= -pi && end_angle > -3 / 2 * pi) {
                    end_angle = -3 / 2 * pi;
                }
                if (end_angle >= -pi && end_angle <= -pi / 2) {
                    end_angle = -pi / 2;
                }
                if (end_angle >= pi && end_angle <= 3 / 2 * pi) {
                    end_angle = 3 / 2 * pi;
                }
                if (end_angle <= pi && end_angle >= pi / 2) {
                    end_angle = pi / 2;
                }

                if (end_angle - start_angle < 0) {
                    end_angle = start_angle;
                }

                if (end_angle - start_angle == pi) {
                    end_angle = start_angle;
                }

                return end_angle;
            };

            var data_arc = d3.svg.arc()
                .innerRadius(function (d, i) {
                return sun_data[1] + r + 30;
            })
                .startAngle(function (d, i) {
                start_angle = calculate_start_angle(i, angle_scale);
                return start_angle;
            })
                .endAngle(function (d, i) {
                end_angle = calculate_end_angle(i, angle_scale);
                return end_angle;
            })
                .outerRadius(function (d, i) {
                radius = sun_data[2] / 100 * rhw + r;
                return radius;
            });

            var data_arc2 = d3.svg.arc()
                .innerRadius(function (d, i) {
                return sun_data[1] + 140;
            })
                .startAngle(function (d, i) {
                start_angle = calculate_start_angle(i, angle_scale);
                return start_angle;
            })
                .endAngle(function (d, i) {
                end_angle = calculate_end_angle(i, angle_scale);
                return end_angle;
            })
                .outerRadius(function (d, i) {
                radius = sun_data[2] / 100 * rhw + 46;
                return radius;
            });

            var sun = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            // scroller rect
            if (_data.length > number_of_data_for_full_graph) {
                sun.append('svg:rect')
                    .attr("x", w / 2 - w / 14)
                    .attr("y", h - h / 32)
                    .attr('width', (w / 2 + w / 14) - (w / 2 - w / 14) + 10)
                    .attr("height", 5)
                    .attr('rx', 4)
                    .attr('ry', 4)
                    .attr('fill', "#ccb5a5")
                    .attr('stroke', "#baa08b");

                var path = sun.append("g").attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");
                path.append('path')
                    .data([{
                        cx: -w / 14
                    }
                ])
                    .attr('d', 'm 0.0389418,0.0432822 9.9610575,0 -0.06029,5.0188999 0,5.2846009 -5.2480518,4.6774 -0.01414,-0.038 L 0,10.005182 0.049611,0.0241822')
                    .attr('fill', '#df5401')
                    .call(dragCircle)
                    .attr('class', 'scroller')
                    .attr('cx', function (d) {
                    return d.cx;
                })
                    .attr("transform", "translate(" + (-w / 14) + ", 0)")
                    .attr('style', 'cursor:pointer');
            }

            sun.selectAll("#" + _element_id)
                .data(_data).enter()
                .append('svg:path')
                .attr('class', 'data')
                .attr("d", data_arc)
                .attr('stroke-width', 1)
                .attr("stroke", "#bab8a9")
                .attr('fill', '#bdcfdb')
                .attr('origin_fill', '#bdcfdb')
                .attr('selectd', 0)
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })
                .on("mouseover", function (d, i) {
                var angle = (calculate_start_angle(parseFloat(d3.select(this).attr('enumerator')), angle_scale) + calculate_end_angle(parseFloat(d3.select(this).attr('enumerator')), angle_scale)) / 2 + pi;
                var radius = sun_data[2] / 100 * rhw + r;
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                var top = (h - h / 8) + Math.cos(angle) * radius;
                var left = w / 2 - Math.sin(angle) * radius;
                var text = d3.select(this).attr('txt');
                graphs.tooltip_show(top, left, text);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click)
                .attr('txt', function (d) {
                return d + "%";
            })
                .attr('enumerator', function (d, i) {
                return i;
            })
                .attr('data_sum', function (d, i) {
                return d3.sum(_data);
            })
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            // in bottom we have the same svg path only smaller..
            sun.selectAll('#' + _element_id)
                .data(_data).enter()
                .append('svg:path')
                .attr('class', 'data2')
                .attr("d", data_arc2)
                .attr('stroke-width', 1)
                .attr('fill', 'none')
                .attr("stroke", "#bab8a9")
                .attr('enumerator', function (d, i) {
                return i;
            })
                .attr('data_sum', function (d, i) {
                return d3.sum(_data);
            })
                .attr("transform", "translate(" + w / 2 + "," + (h - h / 32 * 2) + ")");

            return graphs;
        },

        compare_graphs: function (name, slug, _url) {

            d3.json(host + _url, function (error, json) {
                if (!error) {
                    d3.selectAll("#" + _element_id + " svg").remove();
                    $('#chart').attr('class', '');
                    d3.selectAll("#chart div").remove();
                    var _data2 = [],
                        full_data2 = graphs.populate(json);

                    // map data, first_feature[x] == second_feature[x]
                    for (i = 0; i < full_data.length; i++) {
                        for (j = 0; j < full_data2.length; j++) {
                            if (full_data[i].slug == full_data2[j].slug) {
                                _data2.push(full_data2[j].value);
                                break;
                            }
                        }
                    }
                    graphs.draw_compare_graphs(graphs.current_name, name, _data2);
                    tp.in_graph_select_active_elements();

                } else {
                    console.log("Error on fetch data: ", error.status);
                }
            });
        },

        draw_compare_graphs: function (title1, title2, _data2) {
            /** Compares two graphs.
             *  Current graph info we already know 
             */

            var w = $("#" + _element_id).width(),
                h = $("#" + _element_id).height(),
                rhw = w / 109,
                rwh = h / 109,
                translate_w = w / 16,
                graph_height = h - 15,
                translate = "translate(6," + h + ")";

            var linear = d3.select("#" + _element_id).append("svg:svg")
                .attr("width", w)
                .attr("height", h);

            linear.selectAll("#" + _element_id).data([0]).enter()
                .append("svg:rect")
                .attr('fill', "#e1c8b4")
                .attr('height', graph_height - 25)
                .attr('width', 1)
                .attr("x", 0)
                .attr("y", -graph_height)
                .attr("transform", translate);
            linear.selectAll("#" + _element_id).data([0]).enter()
                .append("svg:text")
                .style("font-size", "12px")
                .style("font-weight", "bold")
                .style("fill", "#bd9267")
                .attr("y", -graph_height + 10)
                .attr("x", 6)
                .text(title2)
                .attr("transform", translate);

            linear.selectAll("#" + _element_id).data([100]).enter()
                .append("svg:rect")
                .attr("fill", "#e1c8b4")
                .attr('width', 100 * rhw)
                .attr('height', 1)
                .attr('y', -25)
                .attr('x', 0)
                .attr("transform", translate);
            linear.selectAll("#" + _element_id).data([0]).enter()
                .append("svg:text")
                .attr("text-anchor", "end")
                .style("font-size", "12px")
                .style("font-weight", "bold")
                .style("fill", "#bd9267")
                .attr("y", -30)
                .text(title1)
                .attr("x", function () {
                return 100 * rhw;
            })
                .attr("transform", translate);


            linear.selectAll('#' + _element_id).data(_data).enter()
                .append('svg:circle')
                .attr('cx', function (d, i) {
                return d * rhw;
            })
                .attr('cy', function (d, i) {
                return -(_data2[i] * rwh + 25);
            })
                .attr('r', 6)
                .attr('fill', '#8bc8b6')
                .attr('origin_fill', '#8bc8b6')
                .attr('selectd', 0)
                .attr('txt', function (d, i) {
                return _data[i] + ' %';
            })
                .attr('name', function (d, i) {
                return full_data[i].slug;
            })
                .on('mouseover', function (d, i) {
                d3.select(this).attr("fill", "#e95201").style('opacity', 0.7);
                graphs.topbar_show(full_data[i].slug);
            })
                .on("mouseout", graphs.on_mouseout)
                .on("click" , graphs.on_click)
                .attr("transform", translate);

            return graphs;
        }

    };
})();