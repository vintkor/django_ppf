$('document').ready(function(){

  // Добавляем клас к header при скроле
  $(document).scroll(function() {
    var scrollWindow = $(document).scrollTop();
    if(scrollWindow > 40){
      $('.header').addClass('header__pinned');
    } else {
      $('.header').removeClass('header__pinned');
    }
  });

  $('.square__not-center').hover(function(event) {
    $(this).toggleClass('active');
  });

  // Cloud parralax
  var cloud = $('#cloud');
  $('body').mousemove(function(event) {
    cloud.css({
      transform: 'translateX(' + event.pageX / 70 + 'px)'
    });
  });

  var typed = new Typed("#typed", {
    stringsElement: '#typed-strings',
    typeSpeed: 60,
    backSpeed: 20,
    backDelay: 500,
    startDelay: 1000,
    loop: true
  });
  
});