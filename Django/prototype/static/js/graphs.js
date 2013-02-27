/**
  * Graph drawing library for Target Price project
  *
  * Usage:
  * graphs.method(url)
  * - method: accuracy/proximity/...
  * - url: url from where to fetch data
  */
var graphs = (function() {

  var _url = '';
  var _element_id = "chart"
  var _data = new Array();
  var _slugs = new Array();
  var _urls = new Array();
  var host = "";

  var _number_of_graphs = 0

  /* Clear the current graph (in case of `active` graph update) */
  d3.selectAll("#" + _element_id + " svg").remove()

  return {

    set_url: function(url) {
      /**
        * Setting url
        * (not sure if needed anymore)
        */
      _url = url
    },

    topbar_show: function(slug) {
      // d3.selectAll(".bank li[class='active']").style('class', 'passive')
      d3.select(".bank li[name='"+slug+"']").style('opacity', 0).transition().duration(400).style('opacity', 1).attr('class', 'active')
    },

    topbar_hide: function() {
      d3.selectAll(".bank li[class='active']").transition().duration(400).attr('class', 'passive')
    },

    tooltip_show: function(top, left, text) {
      /**
        * Show tooltip method
        */
      d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( text )
        .style("left", left + "px") 
        .style("top", top + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
    },

    tooltip_hide: function() {
      /**
        * Hide tooltip method
        */
      d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
    },

    populate: function(json) {

      if ( _number_of_graphs >= 1 ) {

        console.log("dual graph")

      } else {

        console.log("single graph")

        d3.selectAll("#" + _element_id + " svg").remove()

        for (var i = json.length - 1; i >= 0; i--) {
          _data[i] = json[i].value
          _slugs[i] = json[i].analytic__slug
          _urls[i] = json[i].url
        };

        console.log(_slugs)

        /* Foo data */
        // _data = [ 11, 22, 33, 44, 55, 66, 77, 88, 99,11, 22, 33, 44, 55, 66, 77, 88, 99, 11, 22, 33, 44, 55, 66, 77, 88, 99]
        // _data = [99, 99, 99, 99, 1]
        // _data.sort()
        // _slugs = ['foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo']
        // _urls = ['foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo']
      }
      
      _number_of_graphs += 1

      return this
    },

    aggressiveness: function(url) {
      /**
        * Aggressiveness request
        */

      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_aggressiveness();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    profitability: function(url) {
      /**
        * Profitability request
        */
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_profitability();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    accuracy: function(url, phase) {
      /**
        * Accuracy request
        */
      d3.json(host + url, function(error, json) {
        if ( !error ) {
          graphs.populate(json)
          graphs.draw_accuracy(phase);
        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    reach_time: function(url) {
      /**
        * Reach time request
        */
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_reach_time();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    impact_to_stock: function(url) {
      /**
        * Impact to stock request
        */
      d3.json(host + url, function(error, json) {
        if ( !error ) {

          graphs.populate(json)
          graphs.draw_impact_to_stock();

        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    proximity: function(url) {
      /**
        * Proximity graph request
        */

      d3.json(host + url, function(error, json) {
        /* XHR check */
        if ( !error ) {
          /* Populate the data */
          graphs.populate(json)
          /* Draw the graph */
          graphs.draw_proximity();
        } else {
          console.log("Error on fetch data: ", error.status)
        }
      });
      return graphs
    },

    draw_proximity: function() {
      /**
        * Method to draw proximity graphic
        */

      /* Calculate constants */
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
        /* Change to active */
        d3.select(this).style("fill", "#e95201")
        /* Show tooltip */
        var top = w/2+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2
        var left = h/2+parseFloat(d3.select(this).attr('cy')) - 20
        var text = d3.select(this).attr('txt')
        graphs.tooltip_show(top, left, text)
        /* TODO: REQUEST */
      })
      .on("mouseout", function() {
        d3.select(this).style("fill", "#c0be81");
        graphs.tooltip_hide()
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

      return graphs
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
        var top = h/2+parseFloat(d3.select(this).attr('cy')) - 34
        var left = w/2+parseFloat(d3.select(this).attr('cx')) - 22.5
        var text = d3.select(this).attr('txt')
        graphs.tooltip_show(top, left, text)
      })
      .on("mouseout", function() {
        graphs.tooltip_hide()
        d3.select(this).style("fill", "#c0be81");
      })
      .style('opacity', 0)
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })

      return graphs
    },

    draw_profitability: function() {

      var linear_data = [0, 20, 40, 60, 80, 100];
      _data.sort(function(a,b){return b-a});

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 75,
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
        var top = h+parseFloat(d3.select(this).attr('cy')) - 37
        var left = translate_w+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2
        var text = d3.select(this).attr('txt')
        graphs.tooltip_show(top, left, text)
        $('.bank .corp').text(_slugs[i]);
      })
      .on("mouseout", function() {
        graphs.tooltip_hide()
        d3.select(this).style("fill", "#91bcc5");
      })
      .attr("transform", "translate(" + translate_w + "," + h + ")")
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })
        
      return graphs

    },

    
    draw_accuracy: function() {
    /**
      * Method to draw accuracy
      */

      pi = Math.PI;
      phase = 0
      var sun_data = [0, 20, 40, 60, 80, 100];

      var w = $("#" + _element_id).width() - 20,
        h = $("#" + _element_id).height(),
        r = Math.min(w, h) / 15,
        rhw = Math.min(w,h) / 2,
        color = d3.scale.category20c();

      number_of_data_for_full_graph = 40
      
      line_width = w/7
      rect_w = 20;
      
      if (_data.length <= number_of_data_for_full_graph) {
        angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi/2, pi/2]);
      } else {
        angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi/2-phase, pi-phase]);
      }
      
      line_angle_scale = d3.scale.linear().domain([-w/14, w/14]).range([0, 1/2*pi])

      var dragCircle = d3.behavior.drag()
        .on('dragstart', function(){
          d3.event.sourceEvent.stopPropagation();
          console.log('Start Dragging Circle');
          console.log(d3.event)
        })
        .on('dragend', function(d, i) {
          console.log("Drag end", d.cx)
          d3.select(this).attr('cx', d.cx)
        })
        .on('drag', function(d,i){
          d.cx += d3.event.dx;
          if ( d.cx > w/14 ) {
            d.cx = w/14
          }
          if (d.cx < -w/14) {
            d.cx = -w/14
          }
          d3.select(this).attr('cx', d.cx)
          phase = line_angle_scale(d.cx)
          angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi/2-phase, pi-phase]);
          sun.selectAll("path.data")
            .data(_data)
            .attr("d", data_arc)
        });

      var angle_arc = d3.svg.arc()
        .innerRadius(function(d, i) { return r })
        .outerRadius(function(d, i) { return d/100*rhw+r })
        .startAngle(function(d, i) { 
          return -pi/2
        })
        .endAngle(function(d, i) { 
          return pi/2
        });

      var calculate_start_angle = function(i, angle_scale) {
        start_angle = angle_scale(i)
        if ( start_angle <= -pi && start_angle > -3/2*pi ) {
            start_angle = -3/2*pi
          }
          if ( start_angle >= -pi && start_angle <= -pi/2) {
            start_angle = -pi/2
          }
          if ( start_angle >= pi && start_angle <= 3/2*pi ) {
            start_angle = 3/2*pi
          }
          if ( start_angle <= pi && start_angle >= pi/2) {
            start_angle = pi/2
          }
          return start_angle
      }

      var calculate_end_angle = function(i, angle_scale) {
        end_angle = angle_scale(i+1)
        start_angle = calculate_start_angle(i, angle_scale)

        if ( end_angle <= -pi && end_angle > -3/2*pi ) {
          end_angle = -3/2*pi
        }
        if ( end_angle >= -pi && end_angle <= -pi/2) {
          end_angle = -pi/2
        }
        if ( end_angle >= pi && end_angle <= 3/2*pi ) {
          end_angle = 3/2*pi
        }
        if ( end_angle <= pi && end_angle >= pi/2) {
          end_angle = pi/2
        }

        if ( end_angle - start_angle < 0 )  {
          end_angle = start_angle
        }

        if ( end_angle - start_angle == pi ) {
          end_angle = start_angle
        }

        return end_angle
      }
      
      var data_arc = d3.svg.arc()
        .innerRadius(function(d, i) { return r })
        .startAngle(function(d, i) {
          start_angle = calculate_start_angle(i, angle_scale);
          return start_angle
        })
        .endAngle(function(d, i) {
          end_angle = calculate_end_angle(i, angle_scale)
          return end_angle
        })
        .outerRadius(function(d, i) {

          radius = r;

          if (Math.abs(calculate_start_angle(i, angle_scale) - calculate_end_angle(i, angle_scale)) != 0) {
            radius = d/100*rhw+r;
          }

          return radius
        })

      var sun = d3.select("#"+_element_id).append("svg:svg")
        .attr("width", w)
        .attr("height", h);

      if (_data.length > number_of_data_for_full_graph) {
        sun.append('svg:line')
          .attr("x1", w/2-w/14)
          .attr("y1", h-h/32)
          .attr('x2', w/2+w/14)
          .attr("y2", h-h/32)
          .attr('stroke', "black")
          .attr("width", w/2)
          .attr("height", 1)

        var circle = sun.append("g");
        circle.selectAll("circle").data([{cx: -w/14, cy: h/32}])
          .enter().append('circle')
          .attr('cx', function(d){ return d.cx })
          .attr('cy', function(d){ return d.cy })
          .attr('r', 8)
          .call(dragCircle)
          .attr('fill', 'blue')
          .attr("transform", "translate(" + w/2 + "," + (h - h/32*2) + ")")
      }
      

      sun.selectAll('#'+_element_id)
        .data(sun_data).enter()
        .append('svg:path')
        .attr("d", angle_arc )
        .attr('stroke-width', 0.3)
        .attr('fill', 'transparent')
        .attr("stroke", "grey")
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2) + ")")

      sun.selectAll("#" + _element_id)
        .data(_data.reverse()).enter()
        .append('svg:path')
        .attr('class', 'data')
        .attr("d", data_arc)
        .attr('stroke-width', 1)
        .attr("stroke", "#fff")
        .attr('fill', '#8dc6b3')
        .on("mouseover", function() {
          d3.select(this).attr("fill", "#e95201")
          var angle = (angle_scale(parseFloat(d3.select(this).attr('enumerator')))+angle_scale(parseFloat(d3.select(this).attr('enumerator'))+1))/2-pi
          var radius = parseFloat(d3.select(this).attr('txt'))
          var top = (h-h/8)+Math.cos(angle)*(radius*rhw/100+r)
          var left = w/2-Math.sin(angle)*(radius*rhw/110+r)
          var text = d3.select(this).attr('txt')
          graphs.tooltip_show(top, left, text)
        })
        .on("mouseout", function() {
          d3.select(this).attr("fill", "#8dc6b3")
          graphs.tooltip_hide()
        })
        .attr('txt', function(d) { return d })
        .attr('enumerator', function(d, i) { return i })
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2)+ ")")

      return graphs
    },

    draw_reach_time: function() {
    /**
      * Method to draw reach time
      */

      var linear_data = [0, 20, 40, 60, 80, 100];
      _data.sort(function(a,b){return b-a});

      var mouse_click = 0

      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 75,
      color = d3.scale.category20c();

      translate_w = w/16;
      graph_height = h-50;
      number_of_data_for_scroll = 12

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
      .attr('y', function(d, i) { return -graph_height/(_data.length+1)*(i+1) } )
      .attr('x', function(d, i) { return 0 } )
      .attr('txt', function(d,i) { return d + ' %' })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll('#' + _element_id).data(_data).enter()
      .append('svg:circle')
      .attr('cx', function(d, i) {
        return d*rhw
      })
      .attr('cy', function(d, i) {
        return -graph_height/(_data.length+1)*(i+1)
      })
      .attr('r', function(d, i) {
        return 7;
      })
      .attr('fill', '#91bcc5')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        var top = h+parseFloat(d3.select(this).attr('cy')) - 61
        var left = translate_w/3*2+parseFloat(d3.select(this).attr('cx')) - 50
        var text = d3.select(this).attr('txt')
        graphs.tooltip_show(top, left, text)
        graphs.topbar_hide()
        graphs.topbar_show(_slugs[i])
        // text block
        $('.bank .corp').text(_slugs[i]);
      })
      .on("mouseout", function() {

        // graphs.topbar_hide()
        d3.select(this).style("fill", "#91bcc5");
        graphs.tooltip_hide()

      })
      .on("click", function() {

        d3.select(this).style("fill", "#e95201")
      })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      return graphs
    },

    draw_impact_to_stock: function() {
    /**
      * Method to draw impact to market
      */
      pi = Math.PI;

      phase = 0

      var sun_data = [0, 40, 100];

      var w = $("#" + _element_id).width() - 20,
        h = $("#" + _element_id).height(),
        r = Math.min(w,h) / 4,
        rhw = Math.min(w,h) / 4,
        color = d3.scale.category20c();
      
      number_of_data_for_full_graph = 4

      line_width = w/7
      rect_w = 20;
      // if (_data.length <= number_of_data_for_full_graph) {
      //   angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi/2, pi/2]);
      // } else {
      //   angle_scale = d3.scale.linear().domain([0, _data.length]).range([-pi/2-phase, pi-phase]);
      // }

      if ( _data.length <= number_of_data_for_full_graph ) {
        angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi/2, pi/2]);
      } else {
        angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi/2-phase, pi-phase]);
      }
      
      line_angle_scale = d3.scale.linear().domain([-w/14, w/14]).range([0, 1/2*pi])

      var dragCircle = d3.behavior.drag()
        .on('dragstart', function(){
          d3.event.sourceEvent.stopPropagation();
          console.log('Start Dragging Circle');
          console.log(d3.event)
        })
        .on('dragend', function(d, i) {
          console.log("Drag end", d.cx)
          d3.select(this).attr('cx', d.cx)
        })
        .on('drag', function(d,i){
          d.cx += d3.event.dx;
          if ( d.cx > w/14 ) {
            d.cx = w/14
          }
          if (d.cx < -w/14) {
            d.cx = -w/14
          }
          d3.select(this).attr('cx', d.cx)
          phase = line_angle_scale(d.cx)
          angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-pi/2-phase, pi-phase]);
          sun.selectAll("path.data")
            .data(_data)
            .attr("d", data_arc)
        });

      var angle_arc = d3.svg.arc()
        .innerRadius(function(d, i) { return r })
        .outerRadius(function(d, i) { return d/100*rhw+r })
        .startAngle(function(d, i) { 
          return -pi/2
        })
        .endAngle(function(d, i) { 
          return pi/2
        });

      console.log("Data sum:", d3.sum(_data))

      var calculate_start_angle = function(i, angle_scale) {
        angle_sum = 0

        for (var k=0; i-1 >= k; ++k) {
          angle_sum += _data[k]
        }

        start_angle = angle_scale(angle_sum)

        if ( start_angle <= -pi && start_angle > -3/2*pi ) {
            start_angle = -3/2*pi
          }
          if ( start_angle >= -pi && start_angle <= -pi/2) {
            start_angle = -pi/2
          }
          if ( start_angle >= pi && start_angle <= 3/2*pi ) {
            start_angle = 3/2*pi
          }
          if ( start_angle <= pi && start_angle >= pi/2) {
            start_angle = pi/2
          }
          return start_angle
      }

      var calculate_end_angle = function(i, angle_scale) {
        angle_sum = 0
        
        for (var k=0; i >= k; ++k) {
          angle_sum += _data[k]
        };

        console.log("End angle sum:", angle_sum)

        end_angle = angle_scale(angle_sum)
        start_angle = calculate_start_angle(i, angle_scale)

        if ( end_angle <= -pi && end_angle > -3/2*pi ) {
          end_angle = -3/2*pi
        }
        if ( end_angle >= -pi && end_angle <= -pi/2) {
          end_angle = -pi/2
        }
        if ( end_angle >= pi && end_angle <= 3/2*pi ) {
          end_angle = 3/2*pi
        }
        if ( end_angle <= pi && end_angle >= pi/2) {
          end_angle = pi/2
        }

        if ( end_angle - start_angle < 0 )  {
          end_angle = start_angle
        }

        if ( end_angle - start_angle == pi ) {
          end_angle = start_angle
        }

        return end_angle
      }
      
      var data_arc = d3.svg.arc()
        .innerRadius(function(d, i) { return sun_data[1]+r })
        .startAngle(function(d, i) {
          start_angle = calculate_start_angle(i, angle_scale);
          return start_angle
        })
        .endAngle(function(d, i) {
          end_angle = calculate_end_angle(i, angle_scale)
          return end_angle
        })
        .outerRadius(function(d, i) {

          radius = sun_data[2]/100*rhw+r;

          return radius
        })

      var sun = d3.select("#"+_element_id).append("svg:svg")
        .attr("width", w)
        .attr("height", h);

      if ( _data.length > number_of_data_for_full_graph ) {
        sun.append('svg:line')
          .attr("x1", w/2-w/14)
          .attr("y1", h-h/32)
          .attr('x2', w/2+w/14)
          .attr("y2", h-h/32)
          .attr('stroke', "black")
          .attr("width", w/2)
          .attr("height", 1)

        var circle = sun.append("g");
        circle.selectAll("circle").data([{cx: -w/14, cy: h/32}])
          .enter().append('circle')
          .attr('cx', function(d){ return d.cx })
          .attr('cy', function(d){ return d.cy })
          .attr('r', 8)
          .call(dragCircle)
          .attr('fill', 'blue')
          .attr("transform", "translate(" + w/2 + "," + (h - h/32*2) + ")")
      }
      

      sun.selectAll('#'+_element_id)
        .data(sun_data).enter()
        .append('svg:path')
        .attr("d", angle_arc )
        .attr('stroke-width', 0.3)
        .attr('fill', 'transparent')
        .attr("stroke", "grey")
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2) + ")")

      sun.selectAll("#" + _element_id)
        .data(_data.reverse()).enter()
        .append('svg:path')
        .attr('class', 'data')
        .attr("d", data_arc)
        .attr('stroke-width', 1)
        .attr("stroke", "#fff")
        .attr('fill', '#8dc6b3')
        .on("mouseover", function() {
          var angle = (calculate_start_angle(parseFloat(d3.select(this).attr('enumerator')), angle_scale) + calculate_end_angle(parseFloat(d3.select(this).attr('enumerator')), angle_scale) ) /2+pi
          var radius = sun_data[2]/100*rhw+r
          d3.select(this).attr("fill", "#e95201")

          var top = (h-h/8)+Math.cos(angle)*radius
          var left = w/2-Math.sin(angle)*radius
          var text = d3.select(this).attr('txt')
          graphs.tooltip_show(top, left, text)
        })
        .on("mouseout", function() {
          d3.select(this).attr("fill", "#8dc6b3")
          graphs.tooltip_hide()
        })
        .attr('txt', function(d) { return d })
        .attr('enumerator', function(d, i) { return i })
        .attr('data_sum', function(d, i) { return d3.sum(_data) })
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2)+ ")")

      return graphs
    }
  };
})();