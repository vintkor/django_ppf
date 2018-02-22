

$('document').ready(function(){

  function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          // or any other URL that isn't scheme relative or absolute i.e relative.
          !(/^(\/\/|http:|https:).*/.test(url));
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });


  // ---------------------------------- Добавляем клас к header при скроле ----------------------------------

  $(document).scroll(function() {
    var scrollWindow = $(document).scrollTop();
    if(scrollWindow > 40){
      $('.header__wrap').addClass('header__pinned');
    } else {
      $('.header__wrap').removeClass('header__pinned');
    }
  });

  $('.square__not-center').hover(function(event) {
    $(this).toggleClass('active');
  });

  $('.prod_hover').hover(function(event) {
    $(this).toggleClass('active');
  });

  // ---------------------------------- Cloud parralax ----------------------------------
  var cloud = $('#cloud');
  $('body').mousemove(function(event) {
    cloud.css({
      transform: 'translateX(' + event.pageX / 70 + 'px)'
    });
  });

  //  ---------------------------------- Widget last news ----------------------------------

    $(".last-news").owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        navText: ['&larr;', '&rarr;'],
    });

    $(".object-detail__carousel").owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        navText: ['&larr;', '&rarr;'],
    });

});


(function () {
    try {
        new Typed("#typed", {
            stringsElement: '#typed-strings',
            typeSpeed: 60,
            backSpeed: 20,
            backDelay: 500,
            startDelay: 1000,
            loop: true
        });
    } catch(e){}
}());

$('#product-detail__image-wrap').photobox('a',{ time:0 });
$('#product-detail__gallery').photobox('a',{ time:0 });