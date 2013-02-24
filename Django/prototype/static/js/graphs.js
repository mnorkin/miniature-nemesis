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

      // for (var i = json.length - 1; i >= 0; i--) {
      //   _data[i] = json[i].value
      //   _slugs[i] = json[i].slug
      //   _urls[i] = json[i].url
      // };

      _data = [3, 11, 22, 77, 33,  55, 62,  88, 99, 42, 51, 66, 71, 44, 86, 54, 14, 25];

      _slugs = ['foo1', 'foo2', 'foo3', 'foo4', 'foo5', 'foo6', 'foo7', 'foo8', 'foo9', 'foo10', 
                'foo1', 'foo2', 'foo3', 'foo4', 'foo5', 'foo6', 'foo7', 'foo8'];
      _urls = ['foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo']
    },

    /* Agressivness */
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

    accuracy: function(url, phase) {
      d3.json(host + url, function(error, json) {
        if ( !error ) {
          graphs.populate(json)
          graphs.draw_accuracy(phase);
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

    draw_proximity: function() {
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

    draw_aggressiveness: function() {

      var sun_data = [0, 20, 40, 60, 80, 100];

      //_data.sort(function(a,b){return a-b});

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
      .attr("fill", "#FFFBF8")
      .attr("y", function(d) { return -(d/100*rhw+r)-10} )
      .attr("x", function(d) { return -d.toString().length/2*10 } )
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")");

      sun.selectAll("#"+_element_id).data(sun_data).enter()
      .append("svg:text")
      .style("text-anchor", "middle")
      .style("width", "10px")
      .style("height", "10px")
      .style("font-size", "10px")
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
        return 5;
      })
      .attr("transform", "translate(" + w/2 + "," + h/2 + ")")
      .attr('fill', '#71859e')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#"+_element_id)
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", w/2+parseFloat(d3.select(this).attr('cx')) - 22.5 + "px") 
        .style("top", h/2+parseFloat(d3.select(this).attr('cy')) - 34 + "px" )
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
      _data.sort(function(a,b){return b-a});

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 115,
      color = d3.scale.category20c();

      translate_w = w/16;

      var linear = d3.select("#" + _element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      var offset_top = $("#" + _element_id).offset().top - $("#" + _element_id).find('svg').offset().top,
          offset_left = $("#" + _element_id).offset().top - $("#" + _element_id).find('svg').offset().top;

      linear.selectAll("#" + _element_id).data(linear_data).enter()
      .append("svg:rect")
      .attr('fill', "#ece7e3")
      .attr('width', function() { return w-translate_w })
      .attr('height', 1)
      .attr("x", function(d) { return 10} )
      .attr("y", function(d) { return d == 0 ? -10 : -d*rhw-10 } )
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#"+_element_id).data(linear_data).enter()
      .append("svg:text")
      .style("text-anchor", "end")
      .style("width", "10px")
      .style("height", "10px")
      .style("font-size", "10px")
      .style("fill", "#dec7b5")
      .attr("dy", function(d, i) { return d == 0 ? -5 : -d*rhw-5 })
      .attr("dx", function(d, i) { return 5 })
      .text(function(d) { return d })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#" + _element_id).data(_data).enter()
      .append("svg:rect")
      .attr("fill", "#ece7e3")
      .attr('width', 1)
      .attr('height', function(d, i) { return d*rhw })
      .attr('y', function(d, i) { return -d*rhw-10 })
      .attr('x', function(d, i) { return (i+1)*(w-translate_w)/(_data.length+1) })
      .attr("transform", "translate(" + translate_w + "," + h + ")");

      linear.selectAll('#' + _element_id).data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        return (i+1)*(w-translate_w)/(_data.length+1)
      })
      .attr('cy', function(d, i) {
        return -d*rhw-10
      })
      .attr('r', function(d, i) {
        return 5;
      })
      .attr('fill', '#ac8dc6')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#" + _element_id)
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", translate_w+parseFloat(d3.select(this).attr('cx')) - offset_left - 2 + "px") 
        .style("top", h+parseFloat(d3.select(this).attr('cy')) - offset_top - 34 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        .attr("transform", "translate(" + translate_w + "," + h + ")");
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#ac8dc6");
      })
      .attr("transform", "translate(" + translate_w + "," + h + ")");
      

    },

    /* WORK ON THIS */
    draw_accuracy: function( phase ) {

      pi = Math.PI;

      phase = typeof phase !== 'undefined' ? phase : 0;
      var sun_data = [0, 20, 40, 60, 80, 100];

      var w = $("#" + _element_id).width() - 20,
        h = $("#" + _element_id).height()*2,
        h = h-h/32,
        r = Math.min(w, h) / 30,
        rhw = Math.min(w,h) / 2.4,
        color = d3.scale.category20c();
      
      rect_w = 20;
      angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi-phase, pi-phase]);

      var angle_arc = d3.svg.arc()
        .innerRadius(function(d, i) { return r })
        .outerRadius(function(d, i) { return d/100*rhw+r })
        .startAngle(function(d, i) { 
          return -pi/2
        })
        .endAngle(function(d, i) { 
          return pi/2
        });

      var sun = d3.select("#"+_element_id).append("svg:svg")
        .attr("width", w)
        .attr("height", h);

      sun.selectAll('#'+_element_id)
        .data(sun_data).enter()
        .append('svg:path')
        .attr("d", angle_arc )
        .attr('stroke-width', 0.3)
        .attr('fill', 'transparent')
        .attr("stroke", "grey")
        .attr("transform", "translate(" + w/2 + "," + h/2 + ")")

      var circle = sun.selectAll('#' + _element_id)
      .data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        if (angle_scale(i) < pi && angle_scale(i) > -pi) {
          console.log(angle_scale(i))
          return -(d/100*rhw+r)*Math.cos(angle_scale(i))
        } else {
          return 0;
        }
        
      })
      .attr('cy', function(d, i) {
        if (angle_scale(i) < pi && angle_scale(i) > -pi) {
          console.log(angle_scale(i))
          return -(d/100*rhw+r)*Math.sin(angle_scale(i))
        } else {
          return 0;
        }
      })
      .attr('r', function(d, i) {
        if (angle_scale(i) < pi && angle_scale(i) > -pi) {
          console.log(angle_scale(i))
          return 7;
        } else {
          return 0;
        }
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
      .style("opacity", 0)
      .transition().duration(600).style("opacity", 1);

      circle.selectAll(".title")
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })

    },

    draw_reach_time: function() {

      var linear_data = [0, 20, 40, 60, 80, 100];
      _data.sort(function(a,b){return b-a});

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 75,
      color = d3.scale.category20c();

      translate_w = w/16;

      //graph_height = h-(h/8-h/32)
      graph_height = h-50;

      var linear = d3.select("#" + _element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      linear.selectAll("#" + _element_id).data(linear_data).enter()
      .append("svg:rect")
      .attr('fill', "#dec7b5")
      .attr('height', function(){ return graph_height -25; })
      .attr('width', 1)
      .attr("x", function(d, i) { return d*rhw } )
      .attr("y", -graph_height )
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#"+_element_id).data(linear_data).enter()
      .append("svg:text")
      .style("text-anchor", "middle")
      .style("width", "10px")
      .style("height", "10px")
      .style("font-size", "10px")
      .style("fill", "#dec7b5")
      .attr("dy", -10)
      .attr("dx", function(d, i) { return d*rhw + 1; })
      .text(function(d) { return d })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#" + _element_id).data(_data).enter()
      .append("svg:rect")
      .attr("fill", "#dec7b5")
      .attr('width', function(d, i) { return d*rhw })
      .attr('height', 1)
      .attr('y', function(d, i) { return -(i+1)*graph_height/(_data.length) } )
      .attr('x', function(d, i) { return 0 } )
      .attr('txt', function(d,i) { return d + ' %' })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll('#' + _element_id).data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        return d*rhw
      })
      .attr('cy', function(d, i) {
        return -graph_height/(_data.length)*(i+1)
      })
      .attr('r', function(d, i) {
        return 7;
      })
      .attr('fill', '#91bcc5')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", translate_w/3*2+parseFloat(d3.select(this).attr('cx')) - 23 + "px") 
        .style("top", h+parseFloat(d3.select(this).attr('cy')) - 37 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        .attr("transform", "translate(" + translate_w + "," + h + ")");
        // text block
        $('.bank .corp').text(_slugs[i]);
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#91bcc5");
      })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

    },

    draw_impact_to_stock: function() {

    }

  };
})();