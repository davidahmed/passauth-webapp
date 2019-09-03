$(document).ready(function() {
    $(document).submit = false;
    var selected = 0;
    $("#btnFetch").click(function() {
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...'
      );
        setTimeout(function(){
            window.location.replace('success');
        },800);
       
    });

    $(document).on('click', ".choice-option", function(){
    console.log("hi")
    if ($(this).hasClass('thick-border')){
    selected -= 1;
    if (selected <= 1){
        $('#btnFetch').prop('disabled', true)};
        $(this).removeClass('thick-border');
    }
    else{
        $(this).addClass('thick-border');
        selected += 1;
        if (selected >= 1){
        $("#btnFetch").prop('disabled', false);
        }
    }
    });

});


