$(function() {
  
    $.fn.bgfader = function (options) {
        var attrs = {interval:5000, animation:1000};
        attrs = $.extend(attrs, options);

        var bgs = $(this);  
        bgs.css('opacity', '0');
        bgs.first().css('opacity', '1');

        function fadeBg() { 
            for(var i =0; i < bgs.length; i++) {
                var bg = $(bgs[i]);
                if(bg.css('opacity') == 1) {
                    //this is the item;  
                    var next = $(bgs[0]);
                    if(i+1 < bgs.length) {
                        next = $(bgs[i+1]);
                    }
                    bg.animate({opacity:0}, attrs.animation);
                    next.animate({opacity:1}, attrs.animation);
                    break;
                }
            }
        }

        function fadeBgDelay() {
            setTimeout(function() {
                fadeBg();     
                fadeBgDelay();
            }, attrs.interval);
        }

        fadeBgDelay(); 
    }; 


    $('.jumbotron.masthead .background').bgfader();

}); 
