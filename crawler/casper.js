/* Create Casper guy */
var casper = require("casper").create({
    verbose: true,
    logLevel: 'debug'
});
/* Top menu links */
var top_menu_arr = [];
var top_menu_obj = {};
/* The URL of page */
var url = "http://stocktargetprices.com";
/* Alphabet */
var alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
var current_letter = alphabet[Math.floor(Math.random()*alphabet.length)];
/* Top menu selector */
var top_menu_selector = "#mainnav li a";
var companies_list_arr = [];
var companies_list_obj = {};
var page_number = 1;

/**
* Debugging tool to take the screen-shots
***/
function take_screenshot() {
    this.captureSelector("debug.png", "html");
}

/**
* Getting all the links from the main navigation
***/
function get_top_menu() {
    var top_menu_links = document.querySelectorAll("#mainnav li a");
    return Array.prototype.map.call(top_menu_links, function(element) {
        return element.getAttribute("href");
    });
}

/**
* Matching the company list link
***/
function match_companies_link( links ) {
    return Array.prototype.map.call(Array.prototype.filter.call(links, function(link) {
        return (/comp/g).test(link);
    }), function(link) {
        return link;
    });
}

/**
* Matching the login link
***/
function match_login_link( links ) {
    return Array.prototype.map.call(Array.prototype.filter.call(links, function(link) {
        return (/log/g).test(link);
    }), function(link) {
        return link;
    });
}

/**
* List parser
***/
function parse_list() {
    var companies_list = document.querySelectorAll("#company-list ul li a");
    return Array.prototype.map.call(companies_list, function(element) {
        /* TODO: rewrite with regex */
        return {
            'company': element.text.split("(")[0].trim(),
            'market': element.text.split("(")[1].split(")")[0].split(":")[0],
            'ticker': element.text.split("(")[1].split(")")[0].split(":")[1],
            'text': element.text,
            'href': element.href
        };
    });
}

/**
* Checking if we met the last page
***/
function is_this_a_last_page() {
    this.waitForSelector("div.page_nav_bar", function() {
        var pages = this.evaluate(function() {
            // return __utils__.findAll(".page_nav_bar a");
            return document.querySelectorAll(".page_nav_bar a");
        });
        var next_page_number = 0;
        var last_page_number = 0;
        var href = [];

        // this.echo(JSON.stringify(pages));
        this.echo(JSON.stringify(pages[0].innerText));


        last_page_number = this.evaluate(function() {
            return Array.prototype.map.call(Array.prototype.filter.call(pages, function(e) {
                return (e.innerText == 'first');
            }), function(e) {
                return e;
            });
            // return Array.prototype.map.call(Array.prototype.filter.call(pages, function(element) {
            //     href = element.href.split("/");
            //     if ('last' == 'last') {
            //         return true;
            //     }
            // }), function(element) {
            //     // return element.href.split("/")[element.href.split("/").length-1];
            //     return 'lol';
            // });
        });

        // next_page_number = Array.prototype.map.call(Array.prototype.filter.call(pages, function(element) {
        //     href = element.href.split("/");
        //     if (element.innerText.toLowerCase() == 'next') {
        //         return href[href.length-1];
        //     }
        // }), function(element) {
        //     return element;
        // });
        this.echo(last_page_number);
        this.echo(next_page_number);
        if (last_page_number <= next_page_number) {
            return false;
        } else {
            return true;
        }
    });
}

/**
* Go to the page
* Getting everything right with pagination
***/
var go_to_next_page = function() {
    var c_link = url + top_menu_obj.companies_link + '/' + current_letter + '/' + page_number;
    this.open(c_link).then(function() {
        // take_screenshot.call(this);
        // var pages = this.evaluate(function() {
        //     // return __utils__.findAll(".page_nav_bar a");
        //     return document.querySelectorAll(".page_nav_bar a");
        // });

        var last_page = this.evaluate(function() {
            var pages = this.evalute(function() {
                return __utils__.findAll(".page_nav_bar a");
            });
            return pages;
        });
        this.echo(last_page);

        // this.echo(pages[0].innerText);
        // Array.prototype.forEach.call(pages, function(e) {
        //     return e.innerText;
        // });
        // if ( is_this_a_last_page.call(this) ) {
        //     this.echo('This is not the last page');
        //     page_number = page_number + 1;

        //     /**
        //     * Do all the parsing part
        //     ***/
        //     companies_list_arr = this.evaluate(parse_list);
        //     this.echo(JSON.stringify(companies_list_arr));

        // } else {
        //     take_screenshot.call(this);
        //     this.echo('This is the last page');
        //     /**
        //     * Page limit received, need to change the letter and star all over
        //     * again
        //     ***/
        //     page_number = 1;
        //     current_letter = alphabet[Math.floor(Math.random()*alphabet.length)];
        //     // this.run(go_to_next_page);
        // }
        
    });
};

/**
* Starting the engine
***/
casper.start(url);

/**
* After the start, catch all the links from the top menu bar
***/
casper.then(function() {
    top_menu_arr = this.evaluate(get_top_menu);
    top_menu_obj.companies_link = match_companies_link.call(this, top_menu_arr)[0];
    top_menu_obj.login_link = match_login_link.call(this, top_menu_arr)[0];
    /* Go for the companies list link */
});

casper.then(go_to_next_page);


/**
* Final execution and exit
***/
casper.run(function() {
    // this.echo(JSON.stringify(top_menu_obj));
    this.exit();
});
