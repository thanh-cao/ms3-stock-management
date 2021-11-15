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

    if ($('.flash-message')) hideFlashMessages();
});

openSidenav = () => {
    $('nav.sidenav').addClass('show');
    $('nav.sidenav').after('<div class="overlay"></div>')
};

closeSidenav = () => {
    $('nav.sidenav').removeClass('show');
    $('div.overlay').remove();
};

// Function to send ajax request to get data from database based on collection and ObjectId.
// The data is then set to the form's inputs by matching the input's name with the database's field name.
function setValueToFormInputs(form, data) {
    formElements = form[0].elements;

    Object.keys(data).forEach(key => {
        if (formElements[key]) {
            formElements[key].value = data[key];
        }
    })
}

function queryCollection(target, ObjectId) {
    const collection = target.split('_')[1];
    
    switch (collection) {
        case 'user':
            return $.ajax({
                url: '/account/query',
                type: 'POST',
                data: {
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form${target}`), data);
                })
        case 'category':
            return $.ajax({
                url: '/category/query',
                type: 'POST',
                data: {
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form${target}`), data);
                })
        case 'supplier':
            return $.ajax({
                url: '/supplier/query',
                type: 'POST',
                data: {
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form${target}`), data);
                })
    }
}

function showForm(target) {
    target = $(this).attr('data-target');
    $(`${target}`).toggleClass('d-none');
    document.querySelector(target).scrollIntoView({ behavior: 'smooth', block: 'center' });

    // If the show has data-id attribute, create a dynamic form's action based on data-id
    if ($(this).attr('data-id')) {
        baseRoute = `/${$(this).attr('data-target').substring(1)}/`;
        actionRoute = baseRoute + $(this).attr('data-id');
        $(`form${target}`).attr('action', actionRoute);
    };

    // if the form's action is to edit, query the database using ID and set the value to form's inputs
    if (target.includes('edit')) {
        queryCollection(target, $(this).attr('data-id'));
    }
}

function hideForm(target) {
    target = $(this).attr('data-target');
    $(`${target}`).addClass('d-none');
}

function hideFlashMessages() {
    setTimeout(() => {
        $('.flash-message').remove();
    }, 5000)
}