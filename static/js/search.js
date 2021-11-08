// Using ajax to get data from back end and populate search query results with javascript

$('form#product-query').on('submit', function (e) {
    e.preventDefault();

    $.ajax({
        url: '/product/search',
        type: 'POST',
        data: {
            query: $('input#query').val()
        }
    })
        .done(productList => {
            displayProductList(productList);
        })
})

function generateHeading() {
    return `
        <div class="row align-items-center mb-2 g-0">
            <div class="col-6">
                <span class="text-muted ps-2">Product Name</span>
            </div>
            <div class="col-2">
                <span class="text-muted text-center">Current Stock</span>
            </div>
            <div class="col-2">
                <span class="text-muted text-center">Today's change</span>
            </div>
            <div class="col-2"></div>
        </div>`
}

function displayProductList(productLists) {
    let productListHtml = generateHeading();

    productLists.forEach(product => {
        const stockChangeDate = new Date(product.stock_change_date.$date).toDateString();
        const today = new Date().toDateString();
        const stockChange = stockChangeDate === today ? product.stock_change : 0;

        let productRow = `
            <div class="row align-items-center mb-2 py-2 border-bottom g-0 hover-gray">
                <a href="/products/${product._id.$oid}" class="text-decoration-none text-black col-6 ps-2">
                    ${product.name}
                </a>
                <div class="col-2">
                    ${product.current_stock}
                </div>
                <div class="col-2">
                    ${stockChange}
                </div>
                <div class="col-2">
                    <a class="btn text-primary p-0" data-action="showForm" data-target="#update_stock"
                        data-id="${product._id.$oid}">
                        Update Stock
                    </a>
                </div>
            </div>`;

        productListHtml += productRow;
    })

    $('div.product-list').html(productListHtml);
    $('[data-action="showForm"]').on('click', showForm);

    // Add card boder to product list on products.html
    if ($('div.product-list').parent().hasClass('col-12')) {
        $('div.product-list').addClass('card card-body');
    }

    if (productLists.length === 0) {
        $('div.product-list').html('No results found');
    }
}