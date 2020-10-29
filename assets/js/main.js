
/*Toggle dropdown list*/
/*https://gist.github.com/slavapas/593e8e50cf4cc16ac972afcbad4f70c8*/

var navMenuDiv = document.getElementById("nav-content");
var navMenu = document.getElementById("nav-toggle");

document.onclick = check;
function check(e){
    var target = (e && e.target) || (event && event.srcElement);
    
    //Nav Menu
    if (!checkParent(target, navMenuDiv)) {
        // click NOT on the menu
        if (checkParent(target, navMenu)) {
            // click on the link
            if (navMenuDiv.classList.contains("hidden")) {
                navMenuDiv.classList.remove("hidden");
            } else {navMenuDiv.classList.add("hidden");}
        } else {
            // click both outside link and outside menu, hide menu
            navMenuDiv.classList.add("hidden");
        }
    }
    
}
function checkParent(t, elm) {
    while(t.parentNode) {
        if( t == elm ) {return true;}
        t = t.parentNode;
    }
    return false;
}


jQuery(document).ready(function ($) {
  //check if the .cd-image-container is in the viewport
  //if yes, animate it
  checkPosition($(".cd-image-container"));
  $(window).on("scroll", function () {
    checkPosition($(".cd-image-container"));
  });

  //make the .cd-handle element draggable and modify .cd-resize-img width according to its position
  drags(
    $(".cd-handle"),
    $(".cd-resize-img"),
    $(".cd-image-container"),
    $('.cd-image-label[data-type="original"]'),
    $('.cd-image-label[data-type="modified"]')
  );

  //upadate images label visibility
  $(window).on("resize", function () {
    updateLabel(
      $('.cd-image-label[data-type="modified"]'),
      $(".cd-resize-img"),
      "left"
    );
    updateLabel(
      $('.cd-image-label[data-type="original"]'),
      $(".cd-resize-img"),
      "right"
    );
  });
});

function checkPosition(container) {
  if (
    $(window).scrollTop() + $(window).height() * 0.5 >
    container.offset().top
  ) {
    container.addClass("is-visible");
    //you can uncomment the following line if you don't have other events to bind to the window scroll
    // $(window).off('scroll');
  }
}
