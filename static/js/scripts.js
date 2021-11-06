$(document).ready(function () {
    $('button.navbar-toggler').on('click', (e) => {
        e.stopPropagation();
        openSidenav();
    });

    $('[data-action="showForm"]').on('click', showForm);
    $('[data-action="hideForm"]').on('click', hideForm);

    $(document).on('click', (e) => {
        if ($('nav.sidenav').hasClass('show') && !$(e.target).closest('nav.sidenav').length) {
            closeSidenav();
        }
    });
});

openSidenav = () => {
    $('nav.sidenav').addClass('show');
    $('body').css('backgroundColor', 'rgba(0,0,0,0.4)');
};

closeSidenav = () => {
    $('nav.sidenav').removeClass('show');
    $('body').css('backgroundColor', 'rgb(255,255,255)');
};

function showForm(target) {
    target = $(this).attr('data-target');
    $(`${target}`).toggleClass('d-none');
    location.href = `${target}`;

    // If the show has data-id attribute, create a dynamic form's action based on data-id
    if ($(this).attr('data-id')) {
        baseRoute = `/${$(this).attr('data-target').substring(1)}/`;
        actionRoute = baseRoute + $(this).attr('data-id');
        $(`form${target}`).attr('action', actionRoute);
    };
}

function hideForm(target) {
    target = $(this).attr('data-target');
    $(`${target}`).addClass('d-none');
}