var graphs = (function() {

  var _url = '';
  var _element_id = "chart"
  var _data = new Array();
  var _slugs = new Array();
  var _urls = new Array();
  var host = "";

  return {

    set_url: function(url) {
      _url = url
    },

    populate: function(json) {

      for (var i = json.length - 1; i >= 0; i--) {
        _data[i] = json[i].value
        _slugs[i] = json[i].slug
        _urls[i] = json[i].url
      };
    },

    proximity: function(url) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_proximity();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
    },

    profitability: function(url) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_profitability();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
    },

    aggressiveness: function(url) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_aggressiveness();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
    },

    reach_time: function(url) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_reach_time();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
    },

    impact_to_stock: function(url) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_impact_to_stock();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
    },

    accuracy: function(url) {

      d3.json(host + url, function(error, json) {
        if ( !error ) {
          graphs.populate(json)
          graphs.draw_accuracy();
        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });

    },

    draw_accuracy: function() {
      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) /2,
      color = d3.scale.category20c();

      var sun = d3.select("#"+_element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      pi = Math.PI;

      angle_scale = d3.scale.linear().domain([0, _data.length]).range([0, 2*pi])

      angle_arc = d3.svg.arc()
      .innerRadius(r)
      .outerRadius(function(d, i) { return rhw+r })
      .startAngle(function(d, i) { return angle_scale(i)+pi/2 })
      .endAngle(function(d, i) { return angle_scale(i)+pi/2 });

      sun.selectAll('.stripes')
      .data(_data).enter()
      .append('svg:path')
      .attr("d", function(d, i) {
        return angle_arc(d, i)
      })
      .attr('stroke-width', 0.3)
      .attr('fill', 'none')
      .attr("stroke", "grey")
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")")

      sun.selectAll('.stripes')
      .data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        return (d/100*rhw+r)*Math.cos(angle_scale(i))
      })
      .attr('cy', function(d, i) {
        return (d/100*rhw+r)*Math.sin(angle_scale(i))
      })
      .attr('r', function(d, i) {
        return 7;
      })
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")")
      .attr('fill', '#c0be81')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", w/2+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2 + "px") 
        .style("top", h/2+parseFloat(d3.select(this).attr('cy')) - 20 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#c0be81");
      })
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })

      sun.append('circle')
      .style('stroke', 'grey')
      .style('fill', 'white')
      .attr('stroke-width', 0.5)
      .attr('cx', w/2)
      .attr('cy', h/2)
      .attr('r', r);
    },

    draw_proximity: function() {

      var sun_data = [0, 20, 40, 60, 80, 100];

      pi = Math.PI;

      rect_w = 20;

      angle_scale = d3.scale.linear().domain([0, _data.length]).range([0, 2*pi])

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 2.4,
      color = d3.scale.category20c();

      var sun = d3.select("#"+_element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      sun.selectAll("#"+_element_id)
      .data(sun_data).enter().append('circle')
      .style('stroke', '#ece7e3')
      .style('fill', 'transparent')
      .attr('cx', w/2)
      .attr('cy', h/2)
      .attr('r', function(d, i) { return (d/100*rhw+r) })

      sun.selectAll("#"+_element_id).data(sun_data).enter()
      .append("svg:rect")
      .attr("width", function(d) { return d.toString().length*10 })
      .attr("height", 20)
      .attr("fill", "white")
      .attr("y", function(d) { return -(d/100*rhw+r)-10} )
      .attr("x", function(d) { return -d.toString().length/2*10 } )
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")");

      sun.selectAll("#"+_element_id).data(sun_data).enter()
      .append("svg:text")
      .style("text-anchor", "middle")
      .style("width", "10px")
      .style("height", "10px")
      .style("fill", "#dfc8b6")
      .attr("dy", function(d, i) { return -(d/100*rhw+r)+5 })
      .text(function(d) { return d })
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")");

      sun.selectAll('.stripes')
      .data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        return (d/100*rhw+r)*Math.cos(angle_scale(i))
      })
      .attr('cy', function(d, i) {
        return (d/100*rhw+r)*Math.sin(angle_scale(i))
      })
      .attr('r', function(d, i) {
        return 7;
      })
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")")
      .attr('fill', '#71859e')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", w/2+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2 + "px") 
        .style("top", h/2+parseFloat(d3.select(this).attr('cy')) - 20 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#71859e");
      })
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })
      
    },

    draw_profitability: function() {

      var linear_data = [0, 20, 40, 60, 80, 100];

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 200,
      color = d3.scale.category20c();

      var linear = d3.select("#" + _element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      linear.selectAll("#" + _element_id).data(linear_data).enter()
      .append("svg:rect")
      .attr('fill', "black")
      .attr('width', function() { return w-w/16 })
      .attr('height', 1)
      .attr("x", function(d) { return 10} )
      .attr("y", function(d) { return d == 0 ? -10 : -d*rhw-10 } )
      .attr("transform", "translate(" + w/16 + "," + h + ")");

      linear.selectAll("#"+_element_id).data(linear_data).enter()
      .append("svg:text")
      .style("text-anchor", "middle")
      .style("width", "10px")
      .style("height", "10px")
      .style("fill", "#000")
      .attr("dy", function(d, i) { return d == 0 ? -10 : -d*rhw-10 })
      .text(function(d) { return d })
      .attr("transform", "translate(" + w/16 + "," + h + ")");

    },

    draw_aggressiveness: function() {

    },

    draw_reach_time: function() {

    },
    draw_impact_to_stock: function() {

    }

  };
})();