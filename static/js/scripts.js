$(document).ready(function () {
    $('button.navbar-toggler').on('click', (e) => {
        e.stopPropagation();
        openSidenav();
    });

    $(document).on('click', (e) => {
        console.log(e.target);
        if ($('nav.sidenav').hasClass('show') && !$(e.target).closest('nav.sidenav').length) {
            closeSidenav();
        }
    });
});

openSidenav = () => {
    $('nav.sidenav').addClass('show');
    $('body').css('backgroundColor', 'rgba(0,0,0,0.4)');
    console.log('click');
};

closeSidenav = () => {
    $('nav.sidenav').removeClass('show');
    $('body').css('backgroundColor', 'rgb(255,255,255)');
    console.log('close');
};