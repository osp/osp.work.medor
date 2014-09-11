$(function() {
    //Modernizr.load({
        //test: Modernizr.details,
        //yep : 'geo.js',
        //nope: 'geo-polyfill.js'
    //});
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

    var $elts = $('#main-header, #collaborative-experience, #magazine, #accounting');

    $elts.waypoint(function(direction) {
        if (direction === 'down') {
            $(this).addClass('active');
            $(this).waypoint('prev').removeClass('active');
        } else {
            $(this).removeClass('active');
            $(this).waypoint('prev').addClass('active');
        }
    });
});
