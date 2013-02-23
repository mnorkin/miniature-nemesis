/* tested only with 3 entries (target prices) */

// function run_grid() {
// 	// var data = parse_float(get_inner(d3.selectAll(".ac-val").remove()[0]));
// 	// var dataset = [[90, 23, 45], [70, 78, 55], [20, 73, 25]];

// 	var dataset = join_array(parse_float(get_inner(d3.selectAll(".pr-val").remove()[0])), 
// 		parse_float(get_inner(d3.selectAll(".ac-val").remove()[0])), 
// 		parse_float(get_inner(d3.selectAll(".re-val").remove()[0])))

// 	console.log(dataset)

// 	// var count = dataset.length;

// 	// var posName = ['ac', 'pr', 're'];

// 	// var x = d3.scale.linear()
// 	// .domain([0, 100])
// 	// .range([0, 356]);

// 	// var y = d3.scale.ordinal()
// 	// .domain(dataset)
// 	// .rangeBands([0, 36*count]);


// 	// var chart = d3.selectAll('.grid .chart .bar').append('svg')
// 	// .attr('width', 356)
// 	// .attr('height', function(){ return (36*count); })
// 	// .append("g");


// 	// chart.selectAll('rect')
// 	// .data(function(d,i){  return dataset[i]})
// 	// .enter().append('rect')
// 	// .attr('class', function(d,i){ return posName[i]; })
// 	// .attr('height', 12)
// 	// .attr('y', y)
// 	// .attr('rx',4)
// 	// .attr('ry',4)
// 	// .attr('txt', function(d,i){ return d+'%';} )
// 	// .transition().duration(500).attr('width', x)
// 	// .text( String );
// }

function generate_grid_element(id, dataset, posName) {
	if (id != null && dataset != null) {
		dataset = [dataset];
		
		var width = index_page_type == 'list' ? 143 : 356;
		
		var x = d3.scale.linear()
		.domain([0, 500])
		.range([0, width]);
		
		var chart = d3.select("#" + id).append('svg').attr('width', width).attr('height', '20').append('g');
		chart.selectAll('rect')
			.data(dataset)
			.enter().append('rect')
			.attr('class', function(d,i){ return posName[i]; })
			.attr('height', 12)
			.attr('y', 0)
			.attr('rx',4)
			.attr('ry',4)
			.attr('txt', function(d,i){ return d+'%';} )
		.transition().duration(500).attr('width', x)
			.text( String );

	} else {
		return;
	}	
}

function generate_pie(id, value) {
	
	if(index_page_type == 'list'){ return; }
	
	var percent = value;
	var dataset = [percent,(100-percent)];

	var width = 81,
	height = 81,
	radius = Math.min(width, height) / 2;

	var fill_color = "#b7cd44";

	if (value < 0) {
		fill_color = "#da1e1e";
	}

	var colors = [fill_color, 'transparent'];

	

	var pie = d3.layout.pie()
	.sort(null);

	var arc = d3.svg.arc()
	.innerRadius(35)
	.outerRadius(35);

	var svg = d3.selectAll("#" + id).append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

	var path = svg.selectAll("path")
	.data(pie(dataset))
	.enter().append("path")
	.attr("stroke", function(d, i) { return colors[i]; })
	.attr('style', 'fill:none;stroke-width:10; stroke-linejoin:round;')
	.attr("d", arc);
}

/* tested only with 3 entries (target prices) */
function run_list_NENAUDOJAMA(){

	var dataset = [[20, 93, 45], [60, 73, 45], [20, 73, 25]];
	var count = 3;

	var posName = ['ac', 'pr', 're'];

	var width = d3.scale.linear()
	.domain([0, 100])
	.range([0, 143]);

	var x = d3.scale.ordinal()
	.domain(dataset)
	.rangeBands([0, 167*count]);


	var chart = d3.selectAll('.list .chart .bar').append('svg')
	.attr('width', function(){ return (161*count); })
	.attr('height', 18)
	.append("g");


	chart.selectAll('rect')
	.data(function(d,i){  return dataset[i]} )
	.enter().append('rect')
	.attr('class', function(d,i){ return posName[i]; })
	.attr('height', 12)
	.attr('y', 0)
	.attr('x', x)
	.attr('rx',4)
	.attr('ry',4)
	.attr('txt', function(d,i){ return d+'%';} )
	.transition().duration(500).attr('width', width)
	.text( String );
}

function run_grid_pie_NENAUDOJAMA(){

	var percent = 64;
	var dataset = [percent,(100-percent)];

	var width = 81,
	height = 81,
	radius = Math.min(width, height) / 2;

	var colors = ['#da1e1e', 'transparent'];

	var pie = d3.layout.pie()
	.sort(null);

	var arc = d3.svg.arc()
	.innerRadius(35)
	.outerRadius(35);

	var svg = d3.selectAll(".grid .circle").append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

	var path = svg.selectAll("path")
	.data(pie(dataset))
	.enter().append("path")
	.attr("stroke", function(d, i) { return colors[i]; })
	.attr('style', 'fill:none;stroke-width:10; stroke-linejoin:round;')
	.attr("d", arc);

	/* Info http://bl.ocks.org/1346395  http://bl.ocks.org/3750941 */
}


function process_search(dom_obj, e){
	
	// TODO: optimise / cleanup
	e.preventDefault();
	var key = e.keyCode ? e.keyCode : e.charCode
	var obj = $('#search_inp');
	var url = '/search/'+ obj.val();
	if($(dom_obj).attr('type') == "submit"){ alert('soon'); return; }
	if (key == 40 || key == 38){ return process_search_nav(key); }

	if(obj.val() == '') { $('.search_res').html(''); return; }
	
	$.ajax({
	  url: url,
	  dataType: "json",
	}).done(function(resp) {
		console.log(resp, resp.tickers[2])
  		var resp_html = '';
  		
  		if(resp.tickers.length){
  			resp_html += '<li class="inf">Companies</li>';
  		}
  		for(i=0; i < resp.tickers.length ; i++){
  			resp_html += '<li class="entry"><a href="'+resp.tickers[i].url+'">'+resp.tickers[i].name+'</a></li>';
  		}
  		
  		if(resp.analytics.length){
  			resp_html += '<li class="inf">Analytics</li>';
  		}
  		for(i=0; i < resp.analytics.length ; i++){
  			resp_html += '<li class="entry"><a href="'+resp.analytics[i].url+'">'+resp.analytics[i].name+'</a></li>';
  		}
  		
  		$('.search_res').html(resp_html);
	});	
}

function process_search_nav(key){
	if(key == 40){ // nav button down
		var list = $('.search_res li.entry');
		var exit = 0, first_time = ($('.search_res li.active').length == 0);
		
		var i = 0;
		$('.search_res li').each(function(){
			if($(this).hasClass('inf') == 0 && first_time){
				$(this).addClass('active'); exit = 1; first_time = 0;
				$('#search_inp').val($(this).text());
				
				
			}else if ($(this).hasClass('active') && exit == 0){
				var lil = $(this);
					$('#search_inp').val(lil.next().text());
					lil.next().addClass('active');
					lil.removeClass('active');
				exit = 1;
			}
		}); 
		
	}else if(key == 38){
		var list = $('.search_res li.entry');
		var exit = 0, first_time = ($('.search_res li.active').length == 0);
		
		$('.search_res li').each(function(){
			
				
			if ($(this).hasClass('active') && exit == 0){
				var lil = $(this);
					
			 	if(lil.prev().length == 0) { return; }
				lil.removeClass('active');
				lil.prev().addClass('active');
				$('#search_inp').val(lil.prev().text());
				exit = 1;
			}
		}); 
	}
}


/* DOM ready */
$(function(){


	/* Tooltip (percent info box) */
	 $('.chart .bar rect').hover(function(){
	 	var obj = $(this);
	 	var chart = obj.closest('.chart');
	 	var tooltip = chart.children('.bar_tooltip');
	 	
 		var top = obj.offset().top - chart.offset().top - 2;
 		var left = obj.offset().left -chart.offset().left + parseInt(obj.attr('width')) -4; 

	 	tooltip.fadeIn(100);
	 	tooltip.text(obj.attr('txt')).css({top:top,left:left});
	 }, function(){});

	 $('.chart').hover(function(){}, function(){ $('.bar_tooltip').fadeOut(150); });
	 
	 $('body').click(in_graph_click);
	 $('.in_graph').click(in_graph_click);
	 $('.in_graph .sear li').click(in_graph_entry_click);

})

function in_graph_click(){
	var obj = $(this);
	
	if($('.in_graph').hasClass('tmp') ){
		$('.in_graph').removeClass('tmp')
		return;
	}

	if(obj.parents().length > 2){
		obj.addClass('tmp');
		obj.addClass('active');
	}else{
		$('.in_graph').removeClass('active')
	}
}

function in_graph_entry_click(){
	$(this).toggleClass('active');
}

function get_inner( object ) {
	var i, n = object.length;
	for (i=0; i < n; ++i) {
		object[i] = object[i].innerHTML;
	}
	return object;
}

function parse_float( object ) {
	var i, n = object.length;
	for (i=0; i < n; ++i) {
		object[i] = parseFloat(object[i]);
	}
	return object;	
}

function join_array( array0, array1, array2 ) {
	if (array0.length == array1.length && array1.length == array2.length) {
		var i, n = array0.length;
		var object = new Array();

		for (i=0; i < n; ++i) {
			object.push([ array0[i], array1[i], array2[i] ]);
		}

		return object;

	} else {
		console.log(array0.length, array1.length, array2.length);
		return false;
	}
}