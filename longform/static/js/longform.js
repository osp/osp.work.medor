function remy(target) {          
    // Avoids Capitalized short words (2 to 3 characters) to be alone
    pattern = /(\b[A-Z].{0,2}|, .{0,3}) /g;
    text = target.html();          
    target.html(text.replace(pattern, '$1 ')); // I actually put a non-breaking space charcter after $1! You don’t see it, but it’s there. This is to not have this &nbsp; value pop up in places.
}    


$(function() {
    remy($("main"));

    $("#menu").tocify({
        "selectors": "h2",
        "hashGenerator": "pretty"
    });
    
    if (Modernizr.details) {
        console.log('support ok');
    } else {
        console.log('support not ok');
        // script to run if local storage is not supported
    }
    Modernizr.load({
        test: Modernizr.details,
        yep : 'geo.js',
        nope: 'geo-polyfill.js'
    });
    /*
    $("#main").mCustomScrollbar({
        theme:"rounded-dots"
    });
    */

    //$('a[href^="#"]').click(function(){
        //var the_id = $(this).attr("href");
        //scrollTop = $('[id="' + the_id.substring(1) + '"]').position().top - 180;
        //console.log(scrollTop)
        //$('#main').mCustomScrollbar("scrollTo", scrollTop);
        ////$('#main').animate({
        ////    scrollTop:$('[id="' + the_id.substring(1) + '"]').offset().top,
        ////}, 1500);
        //return false;
    //});

    /*
    $.ajax({
        url: 'http://www.kisskissbankbank.com/fr/projects/the-french-fromage/widget',
        type: 'GET',
        success: function(res) {
            var html = $(res.responseText);
            var data = {
                amount: html.find('.amount strong').text(),
                goal: $.trim(html.find('.goal p').contents().filter(function() { return this.nodeType == 3 })[0].textContent),
                collected: $.trim(html.find('.collected p').contents().filter(function() { return this.nodeType == 3 })[0].textContent),
                timeLeft: html.find('.time-left').text(),
                bankers: html.find('.bankers').text()
            }

            var $elt = $('<dl>');

            for (var prop in obj) {
                $el.append($('<dt>').text(prop));
                $el.append($('<dd>').text(obj[prop]));
            }

            console.log($elt);

            $('header').append($elt);
        }
    });
    */
    $('.jcarousel').jcarousel({
        //wrap: 'circular'
    });

    $('.jcarousel-control-prev')
    .jcarouselControl({
        target: '-=1',
    });

    $('.jcarousel-control-next')
    .jcarouselControl({
        target: '+=1',
    });

    var $elts = $('#outer-wrapper, #main-header, #magazine, #collaborative-experience, #accounting');

    $elts.waypoint({
        offset: 70,
        handler: function(direction) {
            if (direction === 'down') {
                var selector = $(this).attr('data-waypoint-target');
                $(selector).addClass('active');

                selector = $(this).waypoint('prev').attr('data-waypoint-target');
                $(selector).removeClass('active');
            } else {
                var selector = $(this).attr('data-waypoint-target');
                $(selector).removeClass('active');

                selector = $(this).waypoint('prev').attr('data-waypoint-target');
                $(selector).addClass('active');
            }
        }
    });

    //$('#panel-acting').waypoint('sticky');

});
