casper = require("casper").create
    viewportSize:
        width: 1024
        height: 786

get_links = ->
    links = document.querySelectorAll("h3.r a")
    Array::map.call links, (e) ->
        try
            (/url\?q=(.*)&sa=U/).exec(e.getAttribute("href"))[1]
        catch e
            e.getAttribute "href"
        

casper.start "http://google.lt", ->
    @fill "form[action=\"/search\"]", q: "casperjs", true

casper.then ->
    # Aggregate results for the 'casperjs' search
    links = @evalute(get_links)