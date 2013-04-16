var casper = require('casper').create({logLevel: "debug"});
//var test_host = 'http://127.0.0.1:8000/';
var test_host = 'http://baklazanas.lt/';

/** Test search **/
casper.start(test_host, function() {

    this.test.assertEvalEqual(function() {
            return document.querySelectorAll('ul.search_res li').length
        }, 0, 'Search box results are empty'
    );

    this.test.assertExists(
        '.search form[method="get"]',
        'Search box form found'
    );

    this.sendKeys('#search_inp', 'a');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('ul.search_res li').length == 12;
            });
        }, 
        function(){
            this.test.assertEvalEqual(function() {
                return document.querySelectorAll('ul.search_res li').length
            }, 12, 'Search box results are 12 entries');
        }
    );

});


/** Test sp500 popup **/
casper.then(function() {  

    this.test.assert(document.querySelectorAll('#popup .list a').length == 0,  'Popup content is empty');

    this.click('a.sp500');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('#popup .list a').length >= 500;
            });
        }, 
        function(){
            this.test.assertEval(function(){
                return document.querySelectorAll('#popup .list a').length >= 500
            }, 'Popup content is more or equal 500 entries');
        },
        function(){ this.test.assert(false, 'Popup content is more or equal 500 entries')}
    );
});



/** Test title target price blocks **/
casper.then(function() { 

    this.test.assertEval(function(){ return document.querySelectorAll('.grid #target-price-list .entry').length >= 3},  
        'Title target price list blocks 3 or more');

    this.test.assertEval(function(){ return document.querySelectorAll('.grid #target-price-list .bar svg').length >= 9},  
        'Title target prices list blocks svg 9 or more');

    // change to list view
    this.click('a.toggle');
    this.test.assertEval(function(){ return document.querySelectorAll('.list #target-price-list .entry').length >= 3},  
        'Title target price grid blocks 3 or more');

    this.test.assertEval(function(){ return document.querySelectorAll('.list #target-price-list .bar svg').length >= 9},  
        'Title target prices grid blocks svg 9 or more');

});


casper.run(function() {
    this.test.renderResults(true);
})
