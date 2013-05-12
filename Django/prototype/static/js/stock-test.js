var current_ticker = $("#current-ticker").text();

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var margin = {
    top: 20,
    right: 20,
    bottom: 30,
    left: 50
};
var width = 900 - margin.left - margin.right;
var height = 300 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;

var start_date = null;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) {
    return x(d.date);
})
    .y(function(d) {
    return y(d.close);
});

var line_open = d3.svg.line()
    .x(function(d) {
        console.log('Stock');
        console.log(x(d.date));
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

d3.json('/api/target_prices/' + current_ticker + '/', function(data) {
    data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.price = d.price;
    });

    x.domain(d3.extent(data, function(d) {
        return d.date;
    }));

    y.domain(d3.extent(data, function(d) {
        return d.close;
    }));

    svg.selectAll("circle")
        .data(data).enter()
        .append('svg:circle')
        .attr('cx', function(d, i) {
            console.log('TP');
            console.log(x(d.date));
            return x(d.date);
        })
        .attr('cy', function(d, i) {
            return d.price;
        })
        .attr('r', 2)
        .attr('fill', '#333');
});

d3.json('/api/stocks/' + current_ticker + '/', function(data) {
    data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.close = d.price_close;
        d.open = d.price_open;
    });

    x.domain(d3.extent(data, function(d) {
        return d.date;
    }));

    y.domain(d3.extent(data, function(d) {
        return d.close;
    }));

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
        .datum(data)
        .attr("class", "line_close")
        .attr("d", line);

    svg.append("path")
        .datum(data)
        .attr('class', 'line_open')
        .attr('d', line_open);

});