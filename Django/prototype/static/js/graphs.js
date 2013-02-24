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

      _data = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99]
      _slugs = ['foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo']
      _urls = ['foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo', 'foo']
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
      rhw = Math.min(w,h) / 115,
      color = d3.scale.category20c();

      translate_w = w/16;

      var linear = d3.select("#" + _element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      linear.selectAll("#" + _element_id).data(linear_data).enter()
      .append("svg:rect")
      .attr('fill', "#dec7b5")
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
      .style("fill", "#dec7b5")
      .attr("dy", function(d, i) { return d == 0 ? -5 : -d*rhw-5 })
      .attr("dx", function(d, i) { return 5 })
      .text(function(d) { return d })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#" + _element_id).data(_data).enter()
      .append("svg:rect")
      .attr("fill", "#dec7b5")
      .attr('width', 1)
      .attr('height', function(d, i) { return d*rhw })
      .attr('y', function(d, i) { return -d*rhw-10 })
      .attr('x', function(d, i) { return (i+1)*(w-translate_w)/(_data.length+1) })
      .attr('txt', function(d,i) { return d + ' %' })
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
        return 7;
      })
      .attr('fill', '#71859e')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", translate_w+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2 + "px") 
        .style("top", h+parseFloat(d3.select(this).attr('cy')) - 20 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        .attr("transform", "translate(" + translate_w + "," + h + ")");
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#71859e");
      })
      .attr("transform", "translate(" + translate_w + "," + h + ")")
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })
      

    },

    
    draw_accuracy: function() {

      pi = Math.PI;

      phase = 0

      var sun_data = [0, 20, 40, 60, 80, 100];

      var w = $("#" + _element_id).width() - 20,
        h = $("#" + _element_id).height(),
        r = Math.min(w, h) / 15,
        rhw = Math.min(w,h) / 2,
        color = d3.scale.category20c();
      
      line_width = w/7
      rect_w = 20;
      angle_scale = d3.scale.linear().domain([0, _data.length]).range([-phase, 2*pi-phase]);
      line_angle_scale = d3.scale.linear().domain([-w/14, w/14]).range([0, 2*pi])

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
          angle_scale = d3.scale.linear().domain([0, _data.length]).range([-phase, 2*pi-phase]);
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

      sun.append('svg:line')
        .attr("x1", w/2-w/14)
        .attr("y1", h-h/32)
        .attr('x2', w/2+w/14)
        .attr("y2", h-h/32)
        .attr('stroke', "black")
        .attr("width", w/2)
        .attr("height", 1)

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
          var element = d3.event.srcElement
          console.log(d3.event)
          console.log(element)
          var angle = (angle_scale(parseFloat(d3.select(this).attr('enumerator')))+angle_scale(parseFloat(d3.select(this).attr('enumerator'))+1))/2-pi
          var radius = parseFloat(d3.select(this).attr('txt'))
          console.log("angle", angle, "radius", radius)
          d3.select(this).attr("fill", "#e95201")
          d3.select("#chart")
            .append('div')
            .attr('class', 'bar_tooltip')
            .text( d3.select(this).attr('txt') + ' %'  )
            .style("left", w/2-Math.sin(angle)*(radius*rhw/110+r) + "px" )
            .style("top", (h-h/8)+Math.cos(angle)*(radius*rhw/100+r) + "px" )
            .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        })
        .on("mouseout", function() {
          d3.select(this).attr("fill", "#8dc6b3")
          d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        })
        .attr('txt', function(d) { return d })
        .attr('enumerator', function(d, i) { return i })
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2)+ ")")

      var circle = sun.append("g");
      circle.selectAll("circle").data([{cx: -w/14, cy: h/32}])
        .enter().append('circle')
        .attr('cx', function(d){ return d.cx })
        .attr('cy', function(d){ return d.cy })
        .attr('r', 8)
        .call(dragCircle)
        .attr('fill', 'blue')
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2) + ")")

      
      // var circle = sun.selectAll('#' + _element_id)
      // .data(_data).enter()
      // .append('svg:circle')
      // .attr('cx', function(d, i) {
      //   // if (angle_scale(i) < pi && angle_scale(i) > -pi) {
          
      //   //   return -(d/100*rhw+r)*Math.cos(angle_scale(i))
      //   // } else {
      //   //   return 0;
      //   // }
      //   return -(d/100*rhw+r)*Math.cos(angle_scale(i))
      // })
      // .attr('cy', function(d, i) {
      //   // if (angle_scale(i) < pi && angle_scale(i) > -pi) {
      //   //   return -(d/100*rhw+r)*Math.sin(angle_scale(i))
      //   // } else {
      //   //   return 0;
      //   // }
      //   return -(d/100*rhw+r)*Math.sin(angle_scale(i))
      // })
      // .attr('r', function(d, i) {
      //   console.log(0, angle_scale(i), pi)
      //   if (angle_scale(i) <= pi && angle_scale(i) >= 0 ) {
      //     return 7;
      //   } else {
      //     return 3;
      //   }
      // })
      // .attr("transform", "translate(" + w/2 + "," + h/2 + ")")
      // .attr('fill', '#c0be81')
      // .attr('txt', function(d,i) { return _data[i] + ' %' })
      // .on('mouseover', function(d, i) {
      //   d3.select(this).style("fill", "#e95201")
      //   d3.select("#chart")
      //   .append('div')
      //   .attr('class', 'bar_tooltip')

      //   .text( d3.select(this).attr('txt') )
      //   .style("left", w/2+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2 + "px") 
      //   .style("top", h/2+parseFloat(d3.select(this).attr('cy')) - 20 + "px" )
      //   .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
      // })
      // .on("mouseout", function() {
      //   d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
      //   d3.select(this).style("fill", "#c0be81");
      // })
      // .style("opacity", 0)
      // .transition().duration(600).style("opacity", 1);

      // TODO: titles
      // sun.selectAll("#" + _element_id).data(_data).enter()
      // .append('title')
      // .text(function(d, i) { return _data[i] + ' %' })

    },

    draw_reach_time: function() {

      var linear_data = [0, 20, 40, 60, 80, 100];
      var w = $("#" + _element_id).width() - 20,
      h = $("#" + _element_id).height() - 40,
      r = Math.min(w, h) / 30,
      rhw = Math.min(w,h) / 43,
      color = d3.scale.category20c();

      translate_w = w/16;

      graph_height = h-(h/8-h/32)

      var linear = d3.select("#" + _element_id).append("svg:svg")
      .attr("width", w)
      .attr("height", h);

      linear.selectAll("#" + _element_id).data(linear_data).enter()
      .append("svg:rect")
      .attr('fill', "#dec7b5")
      .attr('height', h-(h/8-h/32) )
      .attr('width', 1)
      .attr("x", function(d, i) { return d*rhw } )
      .attr("y", -h+h/32 )
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")");

      linear.selectAll("#"+_element_id).data(linear_data).enter()
      .append("svg:text")
      .style("text-anchor", "middle")
      .style("width", "10px")
      .style("height", "10px")
      .style("fill", "#dec7b5")
      .attr("dy", function(d, i) { return 0 })
      .attr("dx", function(d, i) { return d*rhw })
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
      .attr('fill', '#71859e')
      .attr('txt', function(d,i) { return _data[i] + ' %' })
      .on('mouseover', function(d, i) {
        d3.select(this).style("fill", "#e95201")
        d3.select("#chart")
        .append('div')
        .attr('class', 'bar_tooltip')
        .text( d3.select(this).attr('txt') )
        .style("left", translate_w/3*2+parseFloat(d3.select(this).attr('cx')) - d3.select(this).attr('txt').length*3/2 + "px") 
        .style("top", h+parseFloat(d3.select(this).attr('cy')) - 20 + "px" )
        .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        .attr("transform", "translate(" + translate_w + "," + h + ")");
      })
      .on("mouseout", function() {
        d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        d3.select(this).style("fill", "#71859e");
      })
      .attr("transform", "translate(" + translate_w/3*2 + "," + h + ")")
      .append('svg:title')
      .text(function(d, i) { return _data[i] + ' %' })

    },

    /* WORK ON THIS */
    draw_impact_to_stock: function() {
      pi = Math.PI;

      phase = 0

      var sun_data = [0, 40, 100];

      var w = $("#" + _element_id).width() - 20,
        h = $("#" + _element_id).height(),
        r = Math.min(w,h) / 4,
        rhw = Math.min(w,h) / 4,
        color = d3.scale.category20c();
      
      line_width = w/7
      rect_w = 20;
      angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-phase, 2*pi-phase]);
      line_angle_scale = d3.scale.linear().domain([-w/14, w/14]).range([0, 2*pi])

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
          angle_scale = d3.scale.linear().domain([0, d3.sum(_data)]).range([-phase, 2*pi-phase]);
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

      sun.append('svg:line')
        .attr("x1", w/2-w/14)
        .attr("y1", h-h/32)
        .attr('x2', w/2+w/14)
        .attr("y2", h-h/32)
        .attr('stroke', "black")
        .attr("width", w/2)
        .attr("height", 1)

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
          var element = d3.event.srcElement
          console.log(d3.event)
          console.log(element)
          var angle = (angle_scale(parseFloat(d3.select(this).attr('enumerator')))+angle_scale(parseFloat(d3.select(this).attr('enumerator'))+1))/2-pi
          var radius = parseFloat(d3.select(this).attr('txt'))
          console.log("angle", angle, "radius", radius)
          d3.select(this).attr("fill", "#e95201")
          d3.select("#chart")
            .append('div')
            .attr('class', 'bar_tooltip')
            .text( d3.select(this).attr('txt') + ' %'  )
            .style("left", w/2-Math.sin(angle)*(radius*rhw/110+r) + "px" )
            .style("top", (h-h/8)+Math.cos(angle)*(radius*rhw/100+r) + "px" )
            .style('display', "block").style("opacity", 0).transition().duration(200).style("opacity", 1)
        })
        .on("mouseout", function() {
          d3.select(this).attr("fill", "#8dc6b3")
          d3.selectAll("#chart div").transition().duration(400).style("opacity", 0).remove()
        })
        .attr('txt', function(d) { return d })
        .attr('enumerator', function(d, i) { return i })
        .attr('data_sum', function(d, i) { return d3.sum(_data) })
        .attr("transform", "translate(" + w/2 + "," + (h - h/32*2)+ ")")

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
  };
})();