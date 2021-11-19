const searchInput = $('.search');
const matchDisplay = $('.suggestions');
const unitOfMeasurementDisplay = $('.unit-measurement');
const supplierInput = $('#supplier_id');
const deliveryDate = $('#delivery_date');
let products; // declare an empty products variable which will be assigned value in ajax

// Type ahead function is adapted from challange nr6 from Wes Bos' 30-day JavaScript challange
function findMatches(input, productArray) {
    return products.filter(product => {
        // use regular expression to catch user's input and then find matches
        const regex = new RegExp(input, 'gi');
        return product.name.match(regex); // matches with product's name
    });
}

function displayMatches(matches) {
    let matchDisplayHtml = '';
    matches = findMatches(this.value, products);

    matches.forEach(match => {
        let matchRow = `<li class="list-group-item" onclick='select($(this))'>${match.name}</li>`;
        matchDisplayHtml += matchRow;
    });
    matchDisplay.html(matchDisplayHtml);
}

function findProduct(productArray, searchKey) {
    return productArray.filter(obj => Object.keys(obj).some(key => obj[key] === searchKey));
}

function displayUnitOfMeasurement(str) {
    unitOfMeasurementDisplay.removeClass('d-none');
    unitOfMeasurementDisplay.children().first().attr('value', str);
}

function select(option) {
    const selectData = option.text();
    const hiddenInput = $('input[type="hidden"][id="id"]');
    searchInput.val(selectData);

    let found = findProduct(products, selectData);
    hiddenInput.attr('value', found[0]._id.$oid);
    matchDisplay.empty();
    displayUnitOfMeasurement(found[0].unit_of_measurement);
}

function queryProductDatabase() {
    $.ajax({
        url: '/product/query',
        type: 'POST',
        data: {
            query: 'all'
        }
    })
        .done(productList => {
            products = productList;
        });
}

function queryProductFilteredBySupplier(id) {
    sessionStorage.setItem('supplier_id', supplierInput.val());
    id = supplierInput.val();

    $.ajax({
        url: '/product/query',
        type: 'POST',
        data: {
            query: 'supplier',
            supplier_id: id
        }
    })
        .done(productList => {
            products = productList;
        });
}

function removeSessionStorage() {
    ['supplier_id', 'delivery_date'].forEach(item => {
        sessionStorage.removeItem(item);
    });
}

$(document).ready(function () {
    if (location.href.includes('pending-stock')) {
        // If location is either pending-stock/create or pending-stock/edit, query the product database
        // filtered by supplier, save the supplier id and delivery date to session storage. Upon form submission
        // or cancel, remove the session storage
        queryProductFilteredBySupplier(supplierInput.val());

        supplierInput.on('change', queryProductFilteredBySupplier);

        if (sessionStorage.getItem('delivery_date')) {
            deliveryDate.val(sessionStorage.getItem('delivery_date'));
        }

        $('form#create-pending-stock').on('submit', removeSessionStorage);
        $('a.btn[href="/dashboard"]').on('submit', removeSessionStorage);

    } else {
        // query all products in database
        queryProductDatabase();
    }

    searchInput.on('change', displayMatches);
    searchInput.on('keyup', displayMatches);
    deliveryDate.on('change', function () {
        sessionStorage.setItem('delivery_date', deliveryDate.val());
    });
});