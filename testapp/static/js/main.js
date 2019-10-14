//self invoking function
(function()
{
    console.log(data);

    // prevents page from resubmitting form
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
        }
})();