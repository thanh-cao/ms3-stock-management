const searchInput = $('.search');
const matchDisplay = $('.suggestions');

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

function select(option) {
    const selectData = option.text();
    const hiddenInput = $('input[type="hidden"][id="id"]');
    searchInput.val(selectData);

    let found = findProduct(products, selectData);
    hiddenInput.attr('value', found[0]._id.$oid)  
    matchDisplay.empty();
}

$(document).ready(function() {
    searchInput.on('change', displayMatches);
    searchInput.on('keyup', displayMatches);
})
