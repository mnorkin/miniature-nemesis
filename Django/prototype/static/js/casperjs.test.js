var casper = require('casper').create();
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
        'Title target price grid blocks 3 or more');

    this.test.assertEval(function(){ return document.querySelectorAll('.grid #target-price-list .bar svg').length >= 9},  
        'Title target prices grid blocks svg 9 or more');

    // change to list view
    this.click('a.toggle');
    this.test.assertEval(function(){ return document.querySelectorAll('.list #target-price-list .entry').length >= 3},  
        'Title target price list blocks 3 or more');

    this.test.assertEval(function(){ return document.querySelectorAll('.list #target-price-list .bar svg').length >= 9},  
        'Title target prices list blocks svg 9 or more');

});



/** Test ticker page. In this test is apple **/
casper.thenOpen(test_host + 'ticker/aapl/', function(){

    var hash = this.getCurrentUrl().replace(test_host + 'ticker/aapl/', '').split('|');
    this.test.assert(hash[0].length >= 5 && hash[1].length >= 5, 'Ticker page in url have company and feature hash');

    this.test.assertEval(function(){ return document.querySelectorAll('#bank li.active').length === 1},  
        'Ticker page have active/best bank');  

    this.test.assertEval(function(){ return document.querySelectorAll('.analyse_menu div a.active').length === 1},  
        'Ticker page have active feature');

    this.test.assertEval(function(){ return document.querySelectorAll('#chart svg').length === 1},  
        'Ticker page have created graph/svg');

    this.click('.analyse_menu div a.aggressiveness');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('#chart.aggressiveness').length === 1;
            });
        }, 
        function(){
            this.test.assertEval(function(){
                return document.querySelectorAll('#chart.aggressiveness circle').length >= 6;
            }, 'Ticker page loaded aggressiveness graph');
        },
        function(){ this.test.assert(false, 'Ticker page loaded aggressiveness graph')}
    );

    this.test.assertEval(function(){ return document.querySelectorAll('.analyse_menu div.can_compare').length === 1},  
        'Ticker page aggressiveness can compare with one feature'); 

    // click on target prices list in ticker page
    this.click('.inner_buttons a.ta');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('.inner_target_prices li svg').length >= 3;
            });
        }, 
        function(){
            this.test.assertEval(function(){
                return document.querySelectorAll('.inner_target_prices li svg').length >= 3;
            }, 'Ticker page loaded target prices list');
        },
        function(){ this.test.assert(false, 'Ticker page loaded target pricess list')}
    );

});



/** Test analytic page. In this test is citygroup **/
casper.thenOpen(test_host + 'analytic/citigroup/', function(){

    this.test.assertEval(function(){ return document.querySelectorAll('#bank li.active').length === 1},  
        'Analytic page have active/best bank');  

    this.test.assertEval(function(){ return document.querySelectorAll('.analyse_menu div a.active').length === 1},  
        'Analytic page have active feature');

    this.test.assertEval(function(){ return document.querySelectorAll('#chart svg').length === 1},  
        'Analytic page have created graph/svg');


    this.click('.analyse_menu div a.reach_time');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('#chart.reach_time circle').length === document.querySelectorAll('#bank li').length;
            });
        }, 
        function(){
            this.test.assertEval(function(){
                return document.querySelectorAll('#chart.reach_time circle').length === document.querySelectorAll('#bank li').length ;
            }, 'Analytic page circles in reach_time graph are equal to tickers in html');
        },
        function(){ this.test.assert(false, 'Analytic page circles in reach_time graph are equal to tickers in html')}
    );

    // click on target prices list in analytic page
    this.click('.inner_buttons a.ta');
    casper.waitFor(
        function(){
            return this.evaluate(function() {
               return document.querySelectorAll('.inner_target_prices li svg').length >= 3;
            });
        }, 
        function(){
            this.test.assertEval(function(){
                return document.querySelectorAll('.inner_target_prices li svg').length >= 3;
            }, 'Analytic page loaded target prices list');
        },
        function(){ this.test.assert(false, 'Analytic page loaded target pricess list')}
    );

    // test search in analytic page
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
            }, 12, 'Analytic page search returned 12 entries');
        }
    );

});



casper.run(function() {
    this.test.renderResults(true);
})
