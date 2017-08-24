meetup.user = {};

meetup.user.init = function() {
    $('#dashboard-view > div').hide();

    $('#dashboard-nav ul li').click(function(){
        $('#dashboard-nav ul li').removeClass('active');
        $(this).addClass('active');
        $('#dashboard-view > div').hide();
        $('#' + $(this).attr('data-view-id')).show();
    });

    $('#dashboard-nav-profile').click();
    checkHashLocation();

    $(window).on('hashchange', checkHashLocation);
}

var checkHashLocation = function() {
    var hashId = window.location.hash.replace(/#/, '#dashboard-nav-');
    if ($(hashId).length !== 0) {
        $(hashId).click();
    }
}

$(document).ready(function() {
    meetup.user.init();
});