const searchInput = $('.search');
const matchDisplay = $('.suggestions');
const unitOfMeasurementDisplay = $('.unit-measurement');
const supplierInput = $('#supplier_id');
let product; // declare an empty products variable which will be assigned value in ajax

// Type ahead function is adapted from challange nr6 from Wes Bos' 30-day JavaScript challange
function findMatches(input, productArray) {
    return products.filter(product => {
        // use regular expression to catch user's input and then find matches
        const regex = new RegExp(input, 'gi');
        return product.name.match(regex); // matches with product's name
    })
}

function displayMatches(matches) {
    matchDisplayHtml = ''
    matches = findMatches(this.value, products);

    matches.forEach(match => {
        let matchRow = `<li class="list-group-item" onclick='select($(this))'>${match.name}</li>`;
        matchDisplayHtml += matchRow;
    })
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
    hiddenInput.attr('value', found[0]._id.$oid)
    matchDisplay.empty();
    displayUnitOfMeasurement(found[0].unit_of_measurement);
}

function queryProductDatabase() {
    $.ajax({
        url: '/product/search',
        type: 'POST',
        data: {
            query: 'all'
        }
    })
        .done(productList => {
            products = productList;
        })
}

function queryProductFilteredBySupplier(id) {
    sessionStorage.setItem('supplier_id', supplierInput.val());
    id = supplierInput.val();

    $.ajax({
        url: '/product/search',
        type: 'POST',
        data: {
            query: 'supplier',
            supplier_id: id
        }
    })
        .done(productList => {
            products = productList;
        })
}

$(document).ready(function () {
    if (location.href.includes('pending-stock')) {
        supplierInput.on('change', queryProductFilteredBySupplier);
    } else {
        queryProductDatabase();
    }

    searchInput.on('change', displayMatches);
    searchInput.on('keyup', displayMatches);
})