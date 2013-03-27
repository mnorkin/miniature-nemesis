var target_prices_list = [];
var tmp_target_price = {};
var target_price_sort_info = {};
var list_type;
var page_number = Number();

var horizontal_slider_top_offset = 0;
var bottom_of_page = false;
var search_result = {};


function generate_grid_element(id, dataset, posName) {

    if (id !== null && dataset > 1) {
        dataset = [dataset];

        var width = (typeof(list_type) != "undefined" && list_type == 'list') ? 143 : 356;
        var gradiends = {'accuracy': 'url(#first_grad)', 'profitability': 'url(#second_grad)', 'reach_time': 'url(#third_grad)'};

        var max_value = null;

        switch(posName){
            case 'accuracy':
            max_value = 100; break;
            case 'reach_time':
            max_value = 250; break;
            case 'profitability':
            max_value = 100; break;
            default:
            max_value = 10;
        }

        var x = d3.scale.linear()
            .domain([0, max_value])
            .range([0, width]);

        var chart = d3.selectAll("#" + id + ' .'+posName)
            .append('svg')
            .attr('width', width)
            .attr('height', '20')
            .append('g');

        chart.selectAll('rect')
            .data(dataset)
            .enter().append('rect')
            .attr('height', 13)
            .attr('y', 0)
            .attr('fill', gradiends[posName])
            .attr('rx',4)
            .attr('ry',4)
            .attr('txt', function(d,i){
                return (posName == 'reach_time') ? d+' days':  d+'%';
            })
            .transition().duration(500).attr('width', x)
            .text( String );

    } else {
        return;
    }
}


function generate_pie(id, value) {

    if (typeof(list_type) != "undefined" && list_type == 'list'){ return; }

    var percent = value;
    var dataset = [percent];
    var false_dataset = [ 50 ];

    var width = 90,
    height = 90,
    radius = Math.min(width, height) / 2;

    var pi = Math.PI;

    var fill_color = "#b7cd44";

    if (value < 0) {
        fill_color = "#da1e1e";
    }

    var colors = [fill_color, 'transparent'];

    var pie = d3.layout.pie()
        .sort(null);

    var arc = d3.svg.arc()
        .innerRadius(30)
        .outerRadius(40)
        .startAngle(0)
        .endAngle(function(d, i) {
            return 2*pi*(d.value-100)/100;
        });

    var arc2 = d3.svg.arc()
        .innerRadius(0)
        .outerRadius(30)
        .startAngle(0)
        .endAngle(function(d, i) {
            return 2*pi*(d.value-100)/100;
        });

    var arc3 = d3.svg.arc()
        .innerRadius(40)
        .outerRadius(45)
        .startAngle(0)
        .endAngle(function(d, i) {
            return 2*pi*(d.value-100)/100;
        });

    var m_arc = d3.svg.arc()
        .innerRadius(30)
        .outerRadius(40)
        .startAngle(0)
        .endAngle(function(d, i) {
            return 2*pi*(d.value)/100;
        });

    var ellipse_shadow_arc = d3.svg.arc()
        .innerRadius(0)
        .outerRadius(10)
        .startAngle(0)
        .endAngle(function(d, i) {
            return -pi;
        });
    var ellipse_shadow_arc2 = d3.svg.arc()
        .innerRadius(0)
        .outerRadius(10)
        .startAngle(0)
        .endAngle(function(d, i) {
            return pi;
        });

    var angle_scale = d3.scale.linear()
        .domain([0, 100])
        .range([0, pi]);

    var ellipse_shadow_cos_scale = d3.scale.linear()
        .domain([0, pi])
        .range([-35, -35]);

    var ellipse_shadow_sin_scale = d3.scale.linear()
        .domain([0, pi])
        .range([34, 39])

    var svg = d3.select("#" + id + ' .circle').append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var gradient = svg.append('radialGradient')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 40)
        .attr('fx', '0%')
        .attr('fy', '0%')
        .attr('id', 'gradient')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient.append('stop')
        .attr('offset', '60%')
        .attr('style', "stop-color: #b6c64a; stop-opacity: 1");

    gradient.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #c3d75a; stop-opacity: 1');

    var gradient_data_inner = svg.append('radialGradient')
        .attr('cx', 2)
        .attr('cy', 3)
        .attr('r', 40)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'gradient_data_inner')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient_data_inner.append('stop')
        .attr('offset', '70%')
        .attr('style', "stop-color: #fff; stop-opacity: 0.8");

    gradient_data_inner.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #333; stop-opacity: 1');

    var gradient_data_outer = svg.append('radialGradient')
        .attr('cx', 2)
        .attr('cy', 5)
        .attr('r', 39)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'gradient_data_outer')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient_data_outer.append('stop')
        .attr('offset', '60%')
        .attr('style', 'stop-color: #333; stop-opacity: 1');

    gradient_data_outer.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #fff; stop-opacity: 1');

    var gradient3 = svg.append('radialGradient')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 45)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'gradient3')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient3.append('stop')
        .attr('offset', '0%')
        .attr('style', "stop-color: #333; stop-opacity: 1");

    gradient3.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #000; stop-opacity: 0');

    var gradient_inner_empty_down = svg.append('radialGradient')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 45)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'gradient_inner_empty_down')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient_inner_empty_down.append('stop')
        .attr('offset', '50%')
        .attr('style', "stop-color: #333; stop-opacity: 1");

    gradient_inner_empty_down.append('stop')
        .attr('offset', '80%')
        .attr('style', 'stop-color: #d6c4ae; stop-opacity: 0');

    var gradient_inner_empty_out = svg.append('radialGradient')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 45)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'gradient_inner_empty_out')
        .attr('gradientUnits', 'userSpaceOnUse');

    gradient_inner_empty_out.append('stop')
        .attr('offset', '80%')
        .attr('style', 'stop-color: #d6c4ae; stop-opacity: 0');

    gradient_inner_empty_out.append('stop')
        .attr('offset', '100%')
        .attr('style', "stop-color: #333; stop-opacity: 1");

    /* Ellipse gradient */
    var ellipse_gradient = svg.append('radialGradient')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 40)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'ellipse_gradient')
        .attr('gradientUnits', 'userSpaceOnUse');

    ellipse_gradient.append('stop')
        .attr('offset', '70%')
        .attr('style', 'stop-color: #b6c64a; stop-opacity: 1');

    ellipse_gradient.append('stop')
        .attr('offset', '100%')
        .attr('style', "stop-color: #c3d75a; stop-opacity: 1");

    var ellipse_shadow_gradient = svg.append('radialGradient')
        .attr('cx', 2)
        .attr('cy', 1)
        .attr('r', 7)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'ellipse_shadow_gradient')
        .attr('gradientUnits', 'userSpaceOnUse');

    ellipse_shadow_gradient.append('stop')
        .attr('offset', '40%')
        .attr('style', 'stop-color: #333; stop-opacity: 0.4');

    ellipse_shadow_gradient.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #000; stop-opacity: 0');

    var ellipse_shadow_gradient2 = svg.append('radialGradient')
        .attr('cx', 2)
        .attr('cy', 1)
        .attr('r', 6)
        .attr('fx', 0)
        .attr('fy', 0)
        .attr('id', 'ellipse_shadow_gradient2')
        .attr('gradientUnits', 'userSpaceOnUse');

    ellipse_shadow_gradient2.append('stop')
        .attr('offset', '40%')
        .attr('style', 'stop-color: #333; stop-opacity: 0.4');

    ellipse_shadow_gradient2.append('stop')
        .attr('offset', '100%')
        .attr('style', 'stop-color: #000; stop-opacity: 0');

    /* outer shadow */
    svg
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 2)
        .attr('r', 42)
        .attr('stroke-width', 0)
        .attr('fill', 'url(#gradient_data_outer)');


    /* Layer 1 -- global shadow */
    svg
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 2)
        .attr('r', 39)
        .attr('stroke-width', 1)
        .attr('fill', 'url(#gradient3)');

    /* Layer 2 -- Data visualization */
    svg
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 40.1)
        .attr('stroke-width', 0)
        .attr('fill', 'url(#gradient)');

    /* Layer 4 -- overlap data visualization  */
    svg.selectAll('path')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', '#d6c4ae')
        .attr('d', arc);

    /* Inner shadows */
    svg.selectAll('path2')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', 'url(#gradient_inner_empty_down)')
        .attr('d', arc);

    svg.selectAll('path3')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', 'url(#gradient_inner_empty_out)')
        .attr('d', arc);

    /* Layer 5 -- inner circle, to hide the Data visualization main circle */
    svg
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 30)
        .attr('stroke-width', 0)
        .attr('fill', '#fff');

    /* Layer 3 -- Data inner gradient */
    svg
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 30)
        .attr('stroke-width', 0)
        .attr('fill', 'url(#gradient_data_inner)');

    /* Filling inner gradient space */
    svg.selectAll('path4')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', '#fff')
        .attr('d', arc2);

    /* Filling outer gradient fill */
    svg.selectAll('path6')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', '#fff')
        .attr('d', arc3);

    /* Shadow for the ellipse */
    svg.selectAll('path5')
        .data(pie(false_dataset))
        .enter().append('path')
        .attr('fill', 'url(#ellipse_shadow_gradient)')
        .attr('d', ellipse_shadow_arc)
        .attr('transform', 'translate(0, -34)');

    /* Shadow for the ellipse */
    svg.selectAll('path5')
        .data(pie(dataset))
        .enter().append('path')
        .attr('fill', 'url(#ellipse_shadow_gradient2)')
        .attr('d', ellipse_shadow_arc2)
        .attr('transform', function(d) {
            var value = 2*pi*(d.value)/100;
            var sin_angle = ellipse_shadow_sin_scale(value % pi)*Math.sin(value);
            var cos_angle = ellipse_shadow_cos_scale(value % pi)*Math.cos(value);
            return 'translate('+sin_angle+', '+cos_angle+') rotate('+(57*value)+')';
            // return 'translate('+sin_angle+', '+cos_angle+')';
        });

    /* Ellipses to hide the bulky borders in the start and the end */
    svg
        .append('ellipse')
        .attr('cx', 0)
        .attr('cy', -35)
        .attr('rx', 4)
        .attr('ry', 5)
        .attr('fill', 'url(#ellipse_gradient)');

    /* Second ellipse on the end of the data */
    svg.selectAll('ellipse2').data(pie(dataset)).enter()
        .append('ellipse')
        .attr('cx', 0)
        .attr('cy', -35)
        .attr('rx', 4)
        .attr('ry', 5)
        .attr('fill', 'url(#ellipse_gradient)')
        .attr('transform', function(d) {
            console.log(d.value, angle_scale(d.value));
            var value = 360*(d.value)/100;
            return 'rotate('+value+')';
        });

    /* Text */
    svg.selectAll('text').data(dataset)
        .enter().append('text')
        .attr('text-anchor', 'middle')
        .attr('y', 5)
        .attr('x', 0)
        .attr('font-size', '18px')
        .attr('fill', '#b9d240')
        .text(function(d) { console.log(d); return Math.round(d).toString() + '%';});

    /* Shadow for the ellipse2 */
    // svg.selectAll('path7')
    //     .append('path')
    //     .attr('fill', 'url(#ellipse_shadow_gradient')
    //     .attr('d', ellipse_shadow_arc)
    //     .attr('transform', function(d) {
    //         var value = 360*(d.value)/100;
    //         return 'rotate(' + value + ')';
    //     });


    // var path_bottom = svg.selectAll("path")
    //     .data(pie(dataset))
    //     .enter().append("path")
    //     .attr("stroke", function(d, i) { return colors[i]; })
    //     .attr('style', 'fill:#000;stroke-width:10; stroke-linejoin:round;')
    //     .attr("d", arc);

    // var path_top = svg.selectAll("path")
        // .data(pie(dataset))
        // .enter().append("path")
        // .attr("stroke", function(d, i) { return colors[i]; })
        // .attr('style', 'fill:none;stroke-width:10; stroke-linejoin:round;')
        // .attr("d", arc);
}

/*
 * Draw target price block (call d3js)
 */
function process_target_prices_blocks(){
    for(i = 0 ; i < target_prices_list.length ; i++){
        if(target_prices_list[i].processed) { continue; }
        target_prices_list[i].processed = true;
        generate_pie(target_prices_list[i].hash, target_prices_list[i].change);
        generate_grid_element(target_prices_list[i].hash, target_prices_list[i].accuracy, 'accuracy');
        generate_grid_element(target_prices_list[i].hash, target_prices_list[i].profitability, 'profitability');
        generate_grid_element(target_prices_list[i].hash, target_prices_list[i].reach_time, 'reach_time');
    }
}


function process_search(dom_obj, e){
    e.preventDefault();
    var key = e.keyCode ? e.keyCode : e.charCode;
    var obj = $('#search_inp');
    var url = '/search/'+ obj.val()+'/';

    if (key == 40 || key == 38){ process_search_nav(key); return; }
    if($(dom_obj).attr('type') == "submit"){ 
        if($('#search_inp').attr('href') != undefined){ location.href = $('#search_inp').attr('href'); }  
        return false;
    }

    if(obj.val().length < 1) {
        $('.search_res').html('');
        return;
    }

    $.ajax({
        url: url,
        dataType: "json"
    }).done(function(resp) {
        var resp_html = '';
        search_result = resp;

        if(resp.tickers.length){
            resp_html += '<li class="inf"><a onclick="return process_search_page(\'tickers\')" href="">Companies <span>See all</span></a></li>';
            for(i=0; i < resp.tickers.length ; i++){
                if(i >= 5) { break; }
                resp_html += '<li class="entry"><a href="'+resp.tickers[i].url+'">'+resp.tickers[i].name+'</a></li>';
            }
        }

        if(resp.analytics.length) {
            resp_html += '<li class="inf"><a onclick="return process_search_page(\'analytics\')" href="">Analytics<span>See all</span><a/></li>';
            for(i=0; i < resp.analytics.length ; i++){
                if(i >= 5) { break; }
                resp_html += '<li class="entry"><a href="'+resp.analytics[i].url+'">'+resp.analytics[i].name+'</a></li>';
            }
        }

        $('.search_res').html(resp_html);
    });
}

function process_search_nav(key){

    var list = null;
    var first_time = null;
    var i = 0;

    function _set_active(li_obj){
        if(li_obj.length){
            $('.search_res li').removeClass('active');
            li_obj.addClass('active');
            $('#search_inp').val('').val(li_obj.text()).attr('href', li_obj.find('a').attr('href'));
        }
    }

    // nav button down
    if(key == 40){

        list = $('.search_res li');
        first_time = ($('.search_res li.active').length === 0);

        for(i=1 ; i <= list.length ; i++){

            // fist time, no active elements
            if(first_time){
                _set_active( $('.search_res li:nth-child(2)') );
                break;
            }

            if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i+1)+')').hasClass('inf') === false){
                // li nth(i) active and next not have inf class
                _set_active ( $('.search_res li:nth-child('+(i+1)+')') );
                break;
            } else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i+1)+')').hasClass('inf') === true){
                // li nth(i) active and next have inf class     
                _set_active ( $('.search_res li:nth-child('+(i+2)+')') );
                break;
            }
        }

    } else if(key == 38) {

        list = $('.search_res li'), first_time = ($('.search_res li.active').length === 0);
        for(i=1;i <= list.length ; i++){
            // going to input element
            if(i == 2 && $('.search_res li:nth-child('+i+')').hasClass('active')){
                $('.search_res li').removeClass('active');
                // cursor to end
                var tmp_val = $('#search_inp').val(); $('#search_inp').val(tmp_val);
            } else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i-1)+')').hasClass('inf') === false){
                // li nth(i) active and prev not have inf class 
                _set_active ( $('.search_res li:nth-child('+(i-1)+')') );
                break;
            } else if($('.search_res li:nth-child('+i+')').hasClass('active') && $('.search_res li:nth-child('+(i-1)+')').hasClass('inf') === true){
                // li nth(i) active and prev have inf class
                _set_active ( $('.search_res li:nth-child('+(i-2)+')') );
                break;
            }
        }
    }
}

function process_search_page(type){
    var response = '', elem, name, search_resul = search_result[type];

    for (var i = 0; i < search_resul.length; i++) {
        name = (type == 'tickers') ? search_resul[i].name + ' ('+search_resul[i].ticker+')' : search_resul[i].name;
        elem = '<a href="'+search_resul[i].url+'">'+name+'</a>';
        response += elem;
        if(i % 2) { response += '<span></span>'; }
    };
    
    $('#content').html('<div class="search_result"></div>');
    $('#content .search_result').append(response);
    $('#content .search_result').append('<br class="clear" />');
    return false;
}

/**
* Click on property in inner Analyse 
***/
function open_graph(){

    obj = $(this);
    if(obj.hasClass('active')) { return false; }
    var type = obj.parent('div').attr('name');
    var url = obj.attr('href');
    var name = obj.text();
    $('#chart').html('').attr('class', type);
    var graph_fx = eval('graphs.'+type);

    if(typeof(graph_fx) === 'function') {
        graph_fx(url);
        graphs.current_name = name;
        graphs.current_slug = type;
    } else {
        console.log('Graph not ready yet. ' + type);
    }

    $('.analyse_menu a').removeClass('active');
    obj.addClass('active');

    // info box content
    $('.info_box').html( obj.siblings('div').html() );
    show_compare_graph_buttons();
    hash_set_feature(type)
    return false; // prevent href
}

function set_active_analytic(){
    // show first target price
    if($('#bank li.active').length === 0) {
        var name = hash_get('company');
        if(name.length == 0){
            name = graphs.get_best_analytic().slug;
            hash_set_company(name);
        }
        $('#bank li[name='+name+']').addClass('active').removeClass('passive');
        $('.in_graph li[name='+name+']').addClass('active');
    }
}

/** Get from #hash. opt = "company" or opt = "feature" */
function hash_get(opt){
    if(location.hash.length !== 0){
        var name = location.hash.substr(1);
        var arr = name.split('|', 2);
        if(opt == 'company'){ return (arr[0] == undefined) ? '' : arr[0]; }
        else if(opt == 'feature'){ return (arr[1] == undefined) ? '' : arr[1]; }
    }else{
        return '';
    }
}
function hash_set_company(name){
    var feature = hash_get('feature');
    location.hash = '#'+name+'|'+feature;
}
function hash_set_feature(name){
    var company = hash_get('company');
    location.hash = '#'+company+'|'+name;
}

function show_compare_graph_buttons(){
    var current = $('.analyse_menu a.active').attr('class');
    if (current === undefined) { return; }
    current = current.replace('active', '').trim();
    $('.analyse_menu div').removeClass('can_compare');

    switch (current){
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

    $('.analyse_menu .can_compare > span').unbind('click').click(function(){
        var slug = $(this).parent('div').attr('name');
        var url = $(this).siblings('a').attr('href');
        var name = $(this).siblings('a').text();
        graphs.compare_graphs(name, slug, url);
    });
}

function load_target_prices(){

    if($(this).hasClass('active')){ return false; }

    var url = $(this).attr('href');
    $('.inner_buttons a').removeClass('active');
    $(this).addClass('active');

    // load targets and stores Analysis html to temp html container
    if ( url.length ){
        $('.inner_content').animate({'opacity': 0}, 50, function(){
            $(this).addClass('hidden');
            // clear target_prices list
            target_prices_list = [];
            $('.inner_target_prices').load(url, function(){
                $(this).removeClass('hidden');
                $(this).animate({'opacity':1}, 100);
                // loaded fresh content, might need to change type to list
                if (list_type == 'list') {
                    list_type = 'grid';    change_target_prices_list();
                } else {
                    process_target_prices_blocks();
                    binds_for_target_price_list();
                }
            });
        });
        hash_set_feature('target_prices');
        // sets Analysis html back from container
    } else {
        $('.inner_target_prices').animate({'opacity': 0}, 50, function(){
            $(this).addClass('hidden').html('');

            $('.inner_content').removeClass('hidden').css('opacity',0);
            $('.inner_content').animate({'opacity':1}, 100);
        });
        var feature = $('.analyse_menu a.active');
        if(feature.length == 0){  
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
* Because need to rerun javascript for graphs
***/
function change_target_prices_list(){

    var content = null;

    list_type = (list_type == 'list') ? 'grid' : 'list';
    $('.latest_target_prices svg').remove();
    target_prices_list = []; // target prices content will be realoded.
    // set list page
    if($('.latest_target_prices.hidden').hasClass('list')){

        $('.latest_target_prices.list').removeClass('hidden');
        $('.latest_target_prices.grid').addClass('hidden');
        content = $('.latest_target_prices.grid').html();
        $('.latest_target_prices.grid').html('');
        $('.latest_target_prices.list').html(content);
        // set grid page
    }else{
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
            obj.offset().left - chart.offset().left + parseInt(obj.attr('width'), 10) -4);

        tooltip.fadeIn(100);
        tooltip.css({top:top,left:left});
    }, function(){});

    $('.chart').hover(function(){}, function(){ $('.bar_tooltip').fadeOut(150); });

    // long company names moving
    $('.title .entry').hover(
        function() {
           var obj = $(this);
           obj.find('.goust').text(obj.find('.text .slid').text());
           var left = Math.min(0, (165 - obj.find('.goust').width()) );
           obj.find('.text .slid').animate({'left': left}, (left * -15) );
       },
       function(){ $(this).find('.text .slid').stop().css({'left': 0});}
    );
    $('.title .entry').click(function(){ location.href = $(this).find('a').attr('href');});
    $('.latest_target_prices .toggle').unbind('click').click(change_target_prices_list);
    $('.title.list .pre_info span a').unbind('click').click(sort_target_prices);

    // hide company name if it's company page or bank page
    if($('.inner_target_prices').attr('type') !== undefined && $('.latest_target_prices').length !== 0) {
       var obj, who =  $('.inner_target_prices').attr('type');
       $('.inner_target_prices').removeAttr('type');
        $('#target-price-list .entry').each(function(){
            obj = $(this);
            if(who == 'ticker'){
                obj.find('.text .slid').text(obj.find('.analytic').text());
            }
            obj.find('.analytic').text(obj.find('.date').text());
        });
    }
}

function calculate_minavgmax_block(){
    obj = $('.corp_info .avg');
    if(obj.length === 0) { return; }

    var min = obj.find('.mn i').text();
    var avg = obj.find('.av i').text();
    var max = obj.find('.mx i').text();

    // avg element style is from 55 to 250px left; 50 - 246
    //var percent = 195/(max-min)*(avg-min)+55;
    var percent = 196/(max-min)*(avg-min)+50;
    obj.find('.av').css('left',percent);
}

function sort_target_prices(){
    var obj = $(this);
    if(obj.hasClass('active')) { return; }
    $('.title.list .pre_info span a').removeClass('active');
    obj.addClass('active');

    target_price_sort_info.direction = (obj.hasClass('up')) ? 'up' : 'down';
    target_price_sort_info.slug = $(this).parent('span').attr('name');
    var list_html = $('#target-price-list').clone();
    $('#target-price-list').html('');

    // do sort!
    target_prices_list = get_sorted_target_prices(target_prices_list, target_price_sort_info);

    for(i=0 ; i < target_prices_list.length ; i++){
        $('#target-price-list').append(list_html.find('#'+target_prices_list[i].hash));
    }
    binds_for_target_price_list();
}

function get_sorted_target_prices(list, sort_info){
    var new_list = $.extend([], list);

    if(sort_info.direction == 'up'){
        new_list.sort(function(a,b){return b[sort_info.slug]-a[sort_info.slug]; });
    } else {
        new_list.sort(function(a,b){return a[sort_info.slug]-b[sort_info.slug]; });
    }
    return new_list;
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

    // In analyse page, on document ready, load first property or take from hash!
    var feature = hash_get('feature');
    if(feature == 'target_prices'){
        $('.inner_buttons a.ta').trigger('click');
    }else if(feature.length){
        $('.analyse_menu div[name='+feature+'] a').trigger('click');
    }else{
        $('.analyse_menu div:first-child a').trigger('click');
    }

    // long company names moving
    $('.corp_info, .bank .corp').hover(
        function() {
           var obj = $(this);
           obj.find('.goust').text(obj.find('.text .slid').text());
           var left = Math.min(0, (obj.find('.text').width() - 5 - obj.find('.goust').width()) );
           obj.find('.text .slid').animate({'left': left}, (left * -15) );
       },
       function(){ $(this).find('.text .slid').stop().css({'left': 0});}
    );

    // s&p500 index popup
    $('.sp500').click(function(){
        var list = $('#popup .list'), elem;
        $.ajax({
           url: '/tickers/',
           dataType: 'json',
        }).done(function(data){
            $('body').css('overflow', 'hidden');
            $('#popup').show();
            $('#popup .list').height( $('#popup .content').height() - 68);
            for (var i = 0; i < data.length; i++) {
                elem = '<a href="'+data[i].url+'">'+data[i].long_name+' ('+data[i].name+')</a>';
                list.append(elem);
                if(i % 2) { list.append('<span></span>'); }
            };
            list.append('<br class="clear" />');
        });
        return false;
    });
    $('#popup .close, #popup .overlay').click(function(){
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
});


function in_graph_click(){
    var obj = $(this);

    if($('.in_graph').hasClass('tmp') ){
        $('.in_graph').removeClass('tmp');
        return;
    }

    if(obj.parents().length > 2){
        obj.addClass('tmp');
        obj.addClass('active');
        $(".in_graph .sear ul").niceScroll({'cursorborder':'0px', 'cursorcolor':'#cdcdcd', 'cursorwidth': '6px'}); // nice scroll
        $('#ascrail2000, #ascrail2000-hr').css('visibility', 'visible'); // nice scroll
    }else{
        $('.in_graph').removeClass('active');
        $('#ascrail2000, #ascrail2000-hr').css('visibility', 'hidden'); // nice scroll
    }
}

function in_graph_entry_click(){
    var obj = $(this);
    var name = obj.attr('name');
    var svg_element = $('#chart svg [name='+name+']');

    if(obj.hasClass('active')){
        obj.removeClass('active');
        svg_element.attr('fill', svg_element.attr('origin_fill')).attr('selectd', 0);
    }else{
        obj.addClass('active');
        svg_element.attr('fill', '#e95201').attr('selectd', 1);
    }
}

function in_graph_get_active_elements(){
    var list = $('.in_graph .sear li');
    var obj, name, active_elements = [];

    list.each(function(){
        obj = $(this);
        name = obj.attr('name');
        if(obj.hasClass('active')){
            active_elements.push(name);
        }
    });
    return [];
    return active_elements;
}

function in_graph_select_active_elements(){
    set_active_analytic(); // for first time. if any

    var list = $('.in_graph .sear li');
    var obj, name, svg_element;

    list.each(function(){
        obj = $(this);
        name = obj.attr('name');
        svg_element = $('#chart svg [name='+name+']');

        if(obj.hasClass('active')){
            svg_element.attr('fill', '#e95201').attr('selectd', 1);
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

    if ( window_scroll > horizontal_slider_top_offset ) {

        if ($('.horizontal_slider').hasClass('absolute')) {
            $('.horizontal_slider').removeClass('absolute');
        }
        if (!$('.horizontal_slider').hasClass('fixed')) {
            $('.horizontal_slider').addClass('fixed');
        }

    } else {
        if ( $('.horizontal_slider').hasClass('absolute')) {
            $('.horizontal_slider').removeClass('fixed');
        }
        if (!$('.horizontal_slider').hasClass('absolute')) {
            $('.horizontal_slider').addClass('absolute');
        }
    }

    // set target prices Date (html element on the right)
    var obj, exit = false;
    $('.target_price_list li').each(function(index, entry) {
        if (exit) { return; }
        obj = $(entry);
        if (
            obj.offset().top <= window_scroll +50 &&
            obj.offset().top + obj.outerHeight() +
            parseInt(obj.css('margin-bottom'), 10) >= window_scroll +50) {
           $('.now').text(obj.attr('name'));
           exit = true;
        }

    });

    /*
    $('.target_price_list').each(function(index, entry) {
        card_group_position = $(entry).position();
        card_group_height = $(entry).height();
        console.log('Index: ', index);
        console.log('Window scroll: ', window_scroll - horizontal_slider_top_offset + 20);
        console.log('Card group top: ', card_group_position.top);
        console.log('card group top+height: ', card_group_position.top + card_group_height);
        if ( window_scroll - horizontal_slider_top_offset + 50 > card_group_position.top &&
        window_scroll - horizontal_slider_top_offset + 50 < card_group_position.top + card_group_height ) {
            $('.now').text($(entry).attr('name'));
        }
    });
    */

}

function load_more_target_prices(){
    // don't use in inner, analyse page
    if($('.inner_target_prices').length) { return false; }

    /* Give it a bigger offset, for better experience */

    if ($(window).scrollTop() + $(window).height() >= $(document).height() &&
        bottom_of_page === false) {
        page_number +=1;
        /* Make a query */
        _url = "/page/" + page_number + "/";
        // TODO: set target price sorting from {target_price_sort_info} variable
        $.ajax({
           url: _url,
           context: $("#target-price-list")
       }).done(function(data){
            $("#target-price-list").append(data);
            // if one loaded page is not enough, bind and process if no more to load.
            if(load_more_target_prices() === false){
                process_target_prices_blocks();
                binds_for_target_price_list();
            }
        }).error(function() {
            bottom_of_page = true;
        });
        return true; // loaded more target prices
    }else{
        return false; // not loaded, enough
    }
}

/**
* Scroll
***/
$(window).scroll(function() {
    if ($('.horizontal_slider').length !== 0 && horizontal_slider_top_offset === 0) {
        horizontal_slider_top_offset = $('.horizontal_slider').offset().top;
    }
    load_more_target_prices();
    scroll_style_elements();
});

/** window resize **/
$(window).resize(function(){
    $('#popup .list').height( $('#popup .content').height() - 68);
});


/** Internet Explorer save console.log() */
if(typeof(console)=="undefined"){var console={log:function(){}};}

function update_ticker_stock( ticker ) {

    if ($(".price_detail") !== undefined) {
        var format_text = '';
        $.getJSON('/get_ticker_data/' + ticker + '/', function(data) {
            /* data.change_direction apraso i kuria puse reikia sukti arrow */
            $('.price').text( data.last_stock_price );
            format_text = data.change + " ( " + data.change_percent + "%)";
            $('.price_detail').text( format_text );
        });
    }
}
