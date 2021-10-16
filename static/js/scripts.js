$(document).ready(function () {
    $('button.navbar-toggler').on('click', (e) => {
        e.stopPropagation();
        openSidenav();
    });

    $('[data-action="showForm"]').on('click', showForm);
    $('[data-action="hideForm"]').on('click', hideForm);

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

function showForm(target) {
    target = $(this).attr('data-target');
    $(`form${target}`).toggleClass('d-none');
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
    $(`form${target}`).addClass('d-none');
    console.log(target);
    console.log($(`form${target}`));
}