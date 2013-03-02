
var list_type;
var page_number = Number();

function generate_grid_element(id, dataset, posName) {
	
	if (id != null && dataset > 1) {
		dataset = [dataset];
		
		var width = (typeof(list_type) != "undefined" && list_type == 'list') ? 143 : 356;
		var gradiends = {'accuracy': 'url(#first_grad)', 'profitability': 'url(#second_grad)', 'reach_time': 'url(#third_grad)'}

		switch(posName){
			case 'accuracy':
				var max_value = 100; break;
			case 'reach_time':
				var max_value = 250; break;
			case 'profitability':
				var max_value = 100; break;
			default:
				var max_value = 10;
		}

		var x = d3.scale.linear()
		.domain([0, max_value])
		.range([0, width]);

		var chart = d3.select("#" + id).append('svg').attr('width', width).attr('height', '20').append('g');
		chart.selectAll('rect')
			.data(dataset)
			.enter().append('rect')
			.attr('height', 13)
			.attr('y', 0)
			.attr('fill', gradiends[posName])
			.attr('rx',4)
			.attr('ry',4)
			.attr('txt', function(d,i){ return (posName == 'reach_time') ? d+' days':  d+'%';} )
		.transition().duration(500).attr('width', x)
			.text( String );

	} else {
		return;
	}	
}


function generate_pie(id, value) {
	
	if (typeof(list_type) != "undefined" && list_type == 'list'){ return; }

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


function process_search(dom_obj, e){
	
	e.preventDefault();
	var key = e.keyCode ? e.keyCode : e.charCode
	var obj = $('#search_inp');
	var url = '/search/'+ obj.val()+'/';
	
	if (key == 40 || key == 38){ process_search_nav(key); return; }
	if($(dom_obj).attr('type') == "submit"){ location.href = $('#search_inp').attr('href');  return; }
	if(obj.val() == '') { $('.search_res').html(''); return; }
	
	$.ajax({
	  url: url,
	  dataType: "json",
	}).done(function(resp) {
  		var resp_html = '';
  		
  		if(resp.tickers.length){
  			resp_html += '<li class="inf">Companies</li>';
	  		for(i=0; i < resp.tickers.length ; i++){
	  			resp_html += '<li class="entry"><a href="'+resp.tickers[i].url+'">'+resp.tickers[i].name+'</a></li>';
	  		}
  		}
  		
  		if(resp.analytics.length){
  			resp_html += '<li class="inf">Analytics</li>';
	  		for(i=0; i < resp.analytics.length ; i++){
	  			resp_html += '<li class="entry"><a href="'+resp.analytics[i].url+'">'+resp.analytics[i].name+'</a></li>';
	  		}
  		}
  		
  		$('.search_res').html(resp_html);
	});	
}

function process_search_nav(key){

	function _set_active(li_obj){
		if(li_obj.length){
			$('.search_res li').removeClass('active');
			li_obj.addClass('active');
			$('#search_inp').val('').val(li_obj.text()).attr('href', li_obj.find('a').attr('href'));
		}
	}

	if(key == 40){ // nav button down
	    
		var list = $('.search_res li'), first_time = ($('.search_res li.active').length == 0);
		for(var i=1 ; i <= list.length ; i++){
			
			// fist time, no active elements
			if(first_time){
				_set_active( $('.search_res li:nth-child(2)') );	
				break;
			}
				
			// li nth(i) active and next not have inf class		
			if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i+1)+')').hasClass('inf') == false){
				_set_active ( $('.search_res li:nth-child('+(i+1)+')') );
				break;
			// li nth(i) active and next have inf class		
			}else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i+1)+')').hasClass('inf') == true){
				_set_active ( $('.search_res li:nth-child('+(i+2)+')') );
				break;
			}
		}
		
	}else if(key == 38){
	
		var list = $('.search_res li'), first_time = ($('.search_res li.active').length == 0);
		for(var i=1 ; i <= list.length ; i++){
			
			// going to input element
			if(i == 2 && $('.search_res li:nth-child('+i+')').hasClass('active')){
				$('.search_res li').removeClass('active');
				// cursor to end
				var tmp_val = $('#search_inp').val(); $('#search_inp').val(tmp_val);	
			// li nth(i) active and prev not have inf class	
			}else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i-1)+')').hasClass('inf') == false){
				_set_active ( $('.search_res li:nth-child('+(i-1)+')') );
				break;
			// li nth(i) active and prev have inf class		
			}else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i-1)+')').hasClass('inf') == true){
				_set_active ( $('.search_res li:nth-child('+(i-2)+')') );
				break;
			}
		}
	}
}

/*
 * Click on property in inner Analyse 
 */
function open_graph(){

	obj = $(this);
	if(obj.hasClass('active')) { return false; }
	var type = obj.attr('class');
	type = type.toLowerCase();
	type = type.replace(' ', '_');
	var url = obj.attr('href');
	$('#chart').html('').attr('class', type);
	var graph_fx = eval('graphs.'+type);

	if(typeof(graph_fx) === 'function') {
		graph_fx(url);
	}else{
		console.log('Graph not ready yet. ' + type)
	}

	// for testing, because of bulk data
	// if(type == 'max_profitability'){
	// 	eval('graphs.aggressiveness("'+url+'");');
	// }

	$('.analyse_menu a').removeClass('active');
	obj.addClass('active');
	// show first target price
	if($('#bank li.active').length == 0){
		$('#bank li:first-child').addClass('active').removeClass('passive');
	}	
	// info box content
	$('.info_box').html( obj.siblings('div').html() );

	return false; // prevent href
}

function load_target_prices(){
	 	if($(this).hasClass('active')){ return false; }
	 		
	 	var url = $(this).attr('href');
	 	$('.inner_buttons a').removeClass('active');
	 	$(this).addClass('active');


	 	// load targets and stores Analysis html to temp html container
	 	if(url.length){ 
		 	$('.inner_content').animate({'opacity': 0}, 50, function(){
		 		$(this).addClass('hidden');
	            
	            $('.inner_target_prices').load(url, function(){
	            	$(this).removeClass('hidden');
	                $(this).animate({'opacity':1}, 100);
	                // loaded fresh content, might need to change type to list
	                if(list_type == 'list'){
	                	list_type = 'grid';	change_target_prices_list();
	                }else{
	                	binds_for_target_price_list();
	                }
	            });
	        });
        // sets Analysis html back from container
	 	}else{
	 		 $('.inner_target_prices').animate({'opacity': 0}, 50, function(){
		 		$(this).addClass('hidden').html('');

            	$('.inner_content').removeClass('hidden').css('opacity',0);
                $('.inner_content').animate({'opacity':1}, 100);
	            });
	 	}

	 	return false;
 }


/*
 * Remove content, add to another list 
 * Because need to rerun javascript for graphs
 */ 
function change_target_prices_list(){

	list_type = (list_type == 'list') ? 'grid' : 'list';
	$('.latest_target_prices svg').remove();

	// set list page
	if($('.latest_target_prices.hidden').hasClass('list')){
		
		$('.latest_target_prices.list').removeClass('hidden');
		$('.latest_target_prices.grid').addClass('hidden');
		var content = $('.latest_target_prices.grid').html()
		$('.latest_target_prices.grid').html('');
		$('.latest_target_prices.list').html(content);
	// set grid page
	}else{
		$('.latest_target_prices.grid').removeClass('hidden');
		$('.latest_target_prices.list').addClass('hidden');
		var content = $('.latest_target_prices.list').html();
		$('.latest_target_prices.list').html('');
		$('.latest_target_prices.grid').html(content);
	}

	// new content, bind again
	binds_for_target_price_list();
	load_more_target_prices();
	scroll_style_elements();
}


function binds_for_target_price_list(){
	/* Tooltip (percent info box) */
	 $('.chart .bar rect').hover(function(){
	 	var obj = $(this);
	 	var chart = obj.closest('.chart');
	 	var tooltip = chart.children('.bar_tooltip');
	 	tooltip.text(obj.attr('txt'));

	 	var bar_cont_width = ($('.latest_target_prices.list.hidden').length) ? 347 : 133;

 		var top = obj.offset().top - chart.offset().top - 3;
 		var left = Math.min(obj.offset().left - chart.offset().left + bar_cont_width - tooltip.width(), 
 							obj.offset().left - chart.offset().left + parseInt(obj.attr('width')) -4); 

	 	tooltip.fadeIn(100);
	 	tooltip.css({top:top,left:left});
	 }, function(){});

	 $('.chart').hover(function(){}, function(){ $('.bar_tooltip').fadeOut(150); });

	  // long company names moving
	 $('.title .entry').hover(
	 	function(){ 
	 		var left = Math.min(0, (125 - $(this).find('.goust').width()) );
	 		$(this).find('.ln span').animate({'left': left}, (left * -15) ); 
	 	},
	 	function(){ $(this).find('.ln span').stop().css({'left': 0})}
	 );
	 $('.title .entry').click(function(){ location.href = $(this).find('a').attr('href'); })
	 $('.latest_target_prices .toggle').unbind('click').click(change_target_prices_list);
}

function calculate_minavgmax_block(){
	obj = $('.corp_info .avg');
	if(obj.length == 0) { return; }

	var min = obj.find('.mn i').text();
	var avg = obj.find('.av i').text();
	var max = obj.find('.mx i').text();
	
	// avg element style is from 55 to 250px left
	var percent = 195/(max-min)*(avg-min)+55;
	obj.find('.av').css('left',percent);
}


/* DOM ready */
$(function(){
	
	 $('body').click(in_graph_click);
	 $('.in_graph').click(in_graph_click);
	 $('.in_graph .sear li').click(in_graph_entry_click);
	 // to clear search proposals
	 $('body').click(function () { $('.search_res').html(''); });
	 $('.analyse_menu a').click(open_graph);
	
	 $('.inner_buttons a').click(load_target_prices);

	 // In analyse page, on document ready, load first property!
	 $('.analyse_menu div:first-child a').trigger('click');
	 
	 binds_for_target_price_list();
	 calculate_minavgmax_block();
	 load_more_target_prices();
	 scroll_style_elements();
});


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
	var obj = $(this);
	var name = obj.attr('name');
	var svg_element = $('#chart svg [name='+name+']');

	if(obj.hasClass('active')){

		obj.removeClass('active');
		svg_element.attr('fill', svg_element.attr('origin_fill') );
		svg_element.removeAttr('origin_fill')
	}else{

		obj.addClass('active');
		svg_element.attr('origin_fill', svg_element.attr('fill'));
		svg_element.attr('fill', '#e95201');
	}
}

function in_graph_select_active_elements(){
	var list = $('.in_graph .sear li');
	var obj, name, svg_element;

	list.each(function(){
		obj = $(this);
		name = obj.attr('name');
		svg_element = $('#chart svg [name='+name+']');

		if(obj.hasClass('active')){
			svg_element.attr('origin_fill', svg_element.attr('fill'));
			svg_element.attr('fill', '#e95201');
		}
	})
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

function scroll_style_elements(){
	// compare and date buttons
	var target_prices = $('#target-price-list');
	if(target_prices.length){
		var btn_top = Math.max(32, $(window).scrollTop() - target_prices.offset().top + 32);
		$('.latest_target_prices .toggle, .latest_target_prices .now').css({'top':btn_top})
	}

}

function load_more_target_prices(){
	// don't use in inner, analyse page
	if($('.inner_target_prices').length) { return false; }
	
	if ( $(window).scrollTop() + $(window).height() >= $(document).height() ) {

		page_number +=1
		/* Make a query */
		_url = "/page/" + page_number + "/"
		$.ajax({
			url: _url,
			context: $("#target-price-list")
		}).done(function(data){
			$("#target-price-list br").before(data);
			binds_for_target_price_list();
		})
	}
}

/**
  * Scroll
  */
$(window).scroll(function() {
	load_more_target_prices();
	scroll_style_elements();
})


/** Internet Explorer save console.log() */
if(typeof(console)=="undefined"){var console={log:function(){}};}