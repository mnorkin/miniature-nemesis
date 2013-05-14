$(document).ready(function() {

    function getDate(d) {
        return new Date(d.date);
    }

    var current_ticker_slug = $("#current-ticker-slug").text();
    var current_analytic_slug = $("#current-analytic-slug").text();

    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 50
    };
    var width = 900 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.time.scale()
        .domain([parseDate('2007-01-01'), new Date()])
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line_close = d3.svg.line()
        .x(function(d) {
        return x(d.date);
    })
        .y(function(d) {
        return y(d.close);
    });

    var line_open = d3.svg.line()
        .x(function(d) {
        return x(d.date);
    })
        .y(function(d) {
        return y(d.open);
    });

    var svg = d3.select("#stock-graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var stocks_data = null;

    d3.json('/api/stocks/' + current_ticker_slug + '/', function(data) {
        data.forEach(function(d) {
            d.date = parseDate(d.date);
            d.close = d.price_close;
            d.open = d.price_open;
        });
        stocks_data = data;

        x.domain([ d3.min(data, function(d) {
            return d.date;
        }), d3.max(data, function(d) {
            return d.date;
        })]);

        // y.domain([
        //     d3.min(data, function(d) {
        //         return d.open;
        //     }),
        //     d3.max(data, function(d) {
        //         return d.open;
        // })]).nice();

        y.domain([0, d3.max(data, function(d) {
            return d.close + d.close*0.50;
        })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Price ($)");

        svg.append("path")
            .attr("class", "line_close")
            .attr("d", line_close(data));

        svg.append("path")
            .attr('class', 'line_open')
            .attr('d', line_open(data));

        d3.json(
            '/api/target_prices/' + current_ticker_slug + '/' + current_analytic_slug + '/', function(data) {
            data.forEach(function(d) {
                d.parsed_date = parseDate(d.date);
                d.date_1 = (parseFloat(d.date.split('-')[0])+1).toString() +
                    '-' + d.date.split('-')[1] +
                    '-' + d.date.split('-')[2];
                d.parsed_date_1 = parseDate(d.date_1);
                d.x_date = x(d.parsed_date);
                d.x_date_1 = x(d.parsed_date_1);
                d.y_price = y(d.price);
                d.start_point = {
                    'parsed_date': x(d.parsed_date),
                    'price': y(d.price)
                };
                d.end_point = {
                    'parsed_date': x(d.parsed_date_1),
                    'price': y(d.price)
                };
            });


            x.domain([ d3.min(data, function(d) {
                return d.parsed_date;
            }), d3.max(data, function(d) {
                return d.parsed_date_1;
            })]);

            svg.selectAll("svg")
                .data(data).enter()
                .append('svg:circle')
                .attr('cx', function(d, i) {
                    return d.x_date;
                })
                .attr('cy', function(d, i) {
                    return d.y_price;
                })
                .attr('r', 2)
                .attr('fill', '#333');

            svg.selectAll("svg")
                .data(data).enter()
                .append('svg:circle')
                .attr('cx', function(d, i) {
                    return d.x_date_1;
                })
                .attr('cy', function(d, i) {
                    return d.y_price;
                })
                .attr('r', 2)
                .attr('fill', '#333');

            svg.selectAll("#stock-graph")
                .data(data).enter()
                .append('svg:line')
                .attr('x1', function(d) {
                    console.log(d.start_point.parsed_date);
                    return d.start_point.parsed_date;
                })
                .attr('y1', function(d) {
                    console.log(d.start_point.price);
                    return d.start_point.price;
                })
                .attr('x2', function(d) {
                    console.log(d.end_point.parsed_date);
                    return d.end_point.parsed_date;
                })
                .attr('y2', function(d) {
                    return d.end_point.price;
                })
                .style('stroke', 'rgb(6,120,155)');

        });

    });

});