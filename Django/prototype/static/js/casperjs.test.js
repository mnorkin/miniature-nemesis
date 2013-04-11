var casper = require('casper').create();

casper.start('http://baklazanas.lt/', function() {

    this.test.assertEvalEqual(function() {
        return document.querySelectorAll('ul.search_res li').length
    }, 0, 'Search box results are hidden'
    );

    this.test.assertExists(
        'form[method="get"]',
        'Search box form found'
    );

    this.sendKeys('input[name="q"]', 'a');

});

casper.then(function() {

    this.test.assertEvalEqual(function() {
        return document.querySelectorAll('ul.search_res li').length;
        },
        12,
        'Search box results is equal to one ticker and title'
    );

    this.test.assertEvalEqual(function() {
        return document.querySelector('div[id="popup"]').style['display']
        },
        '',
        'Popup is hidden'
    );

    this.click('a[class="sp500"]');

});

casper.then(function() { 

    this.test.assertEvalEqual(function() {
            return document.querySelector('div[id="popup"]').style['display']
        },
        'block',
        'Popup is displayed'
    );

});


casper.run(function() {
    this.test.renderResults(true);
})
