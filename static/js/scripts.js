$(document).ready(function () {
    $('button.navbar-toggler').on('click', (e) => {
        e.stopPropagation();
        openSidenav();
    });

    $(document).on('click', (e) => {
        if ($('nav.sidenav').hasClass('show') && !$(e.target).closest('nav.sidenav').length) {
            closeSidenav();
        }
    });

    $('[data-action="showForm"]').on('click', showForm);

    if ($('.flash-message')) hideFlashMessages();
});

function openSidenav() {
    $('nav.sidenav').addClass('show');
    $('nav.sidenav').after('<div class="overlay"></div>');
}

function closeSidenav() {
    $('nav.sidenav').removeClass('show');
    $('div.overlay').remove();
}

// Function to send ajax request to get data from database based on collection and ObjectId.
// The data is then set to the form's inputs by matching the input's name with the database's field name.
function setValueToFormInputs(form, data) {
    let formElements = form[0].elements;

    Object.keys(data).forEach(key => {
        if (formElements[key]) {
            formElements[key].value = data[key];
        }
    });
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
                    setValueToFormInputs($(`form#${target}`), data);
                });
        case 'category':
            return $.ajax({
                url: '/category/query',
                type: 'POST',
                data: {
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form#${target}`), data);
                });
        case 'supplier':
            return $.ajax({
                url: '/supplier/query',
                type: 'POST',
                data: {
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form#${target}`), data);
                });
        case 'product':
            return $.ajax({
                url: '/product/query',
                type: 'POST',
                data: {
                    'query': 'product',
                    'ObjectId': ObjectId
                }
            })
                .done(data => {
                    setValueToFormInputs($(`form#${target}`), data);
                });
    }
}

function showForm(target) {
    target = $(this).attr('data-target');
    $('#form-container').html(window[target]);
    
    // If the show has data-id attribute, create a dynamic form's action based on data-id
    if ($(this).attr('data-id')) {
        const baseRoute = `/${$(this).attr('data-target')}/`;
        const actionRoute = baseRoute + $(this).attr('data-id');
        $(`form#${target}`).attr('action', actionRoute);
    }

    // if the form's action is to edit, query the database using ID and set the value to form's inputs
    if (target.includes('edit')) {
        queryCollection(target, $(this).attr('data-id'));
    }

    if ($('input#received_stock')) {
        activateInputEvent();
    }

    $('[data-action="hideForm"]').on('click', hideForm);
}

function activateInputEvent() {
    // Use ajax to submit stock change on received_stock input's change event
    // This is a pending step to prepare stock change data in the backend with session 'stock'
    // before stock change is actually updated in the database when user clicks approve

    $('input#received_stock').each(function() {
        $(this).on('change', function () {
            $.ajax({
                    url: '/pending-stock/update',
                    type: 'POST',
                    data: {
                        id: $(this).prev().val(),
                        received_stock: $(this).val()
                    }
                })
                .done(function (data) {
                    console.log(data);
                });
        });
    });
}

function hideForm() {
    $('#form-container').empty();
}

function hideFlashMessages() {
    setTimeout(() => {
        $('.flash-message').remove();
    }, 5000);
}