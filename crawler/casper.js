/* Create Casper guy */
var casper = require("casper").create();
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
    var pages = document.querySelectorAll(".page_nav_bar a");
    var next_page_number = 0;
    var last_page_number = 0;
    var href = [];
    Array.prototype.map.call(pages, function(element) {
        href = element.href.split("/");
        if (element.innerText == 'last') {
            last_page_number = href[href.length-1];
        }
        if (element.innerText) {
            next_page_number = href[href.length-1];
        }
    });
    if (last_page_number == next_page_number) {
        return false;
    } else {
        return true;
    }
}

/**
* Go to the page
* Getting everything right with pagination
***/
var go_to_page = function() {
    this.thenOpen(url + top_menu_obj.companies_link + current_letter + page_number, function() {

        if ( is_this_a_last_page.call(this) ) {
            page_number = page_number + 1;
        } else {
            /* Switch to the next letter, if the end of the letter pages was reached */
        }
        
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
    this.thenOpen(url + top_menu_obj.companies_link, function() {
        /* Get the list */
        companies_list_arr = this.evaluate(parse_list);
        this.echo(JSON.stringify(companies_list_arr));
    });
});


/**
* Final execution and exit
***/
casper.run(function() {
    // this.echo(JSON.stringify(top_menu_obj));
    this.exit();
});
