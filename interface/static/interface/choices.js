$(document).ready(function() {

    $("#btnFetch").click(function() {
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...'
      );
        setTimeout(function(){
            window.location.replace('success');
        },1000);
       
    });

    $(document).on('click', ".choice-option", function(){
    console.log("hi")
    if ($(this).hasClass('thick-border')){
    $(this).removeClass('thick-border');
    }
    else{
    $(this).addClass('thick-border');
    }
    });

});


