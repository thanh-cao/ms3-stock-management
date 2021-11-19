// This search.js file contains ajax call to get data from back end and populate search query results with javascript

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
        </div>`;
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
                    <a class="btn text-primary p-0" data-action="showForm" data-target="#edit_product_stock"
                        data-id="${product._id.$oid}">
                        Update Stock
                    </a>
                </div>
            </div>`;

        productListHtml += productRow;
    });

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

function displayPendingStocks(pendingStocks) {
    let pendingStockListHtml = '';
    
    pendingStocks.forEach(pending => {
        const delivery_date = new Date(pending.delivery_date.$date).toDateString();
        const statusHtml = (pending.is_approved) ? '<span class="badge bg-success">Done</span>' : '<span class="badge bg-warning">Pending</span>';
        const supplierName = $('select#supplier_id option:selected').text();
        
        let row = `
        <a href="/pending-stock/${pending._id.$oid}" class="text-decoration-none text-black">
            <div class="row border-bottom align-items-center py-2 g-0 mb-3 hover-gray">
                <div class="col-6 ps-2">
                    ${supplierName}
                </div>
                <div class="col-3 text-center">
                    ${delivery_date}
                </div>
                <div class="col-3 text-center">
                    ${statusHtml}
                </div>
            </div>
        </a>`;

        pendingStockListHtml += row;
    });

    $('.pending-stock-list').html(pendingStockListHtml);

    if (pendingStocks.length === 0) {
        $('.pending-stock-list').html('No results found');
    }
}

// query to get product list
$('form#product-query').on('submit', (e) => {
    e.preventDefault();

    $.ajax({
        url: '/product/query',
        type: 'POST',
        data: {
            query: $('input#query').val()
        }
    })
        .done(productList => {
            displayProductList(productList);
        });
});

$('button.search-pending').on('click', function() {
    $('.search-pending-wrapper').toggleClass('d-none');
});

// query to get pending stock list
$('form#pending-stock-query').on('submit', (e) => {
    e.preventDefault();

    $.ajax({
        url: '/pending-stock/search',
        type: 'POST',
        data: {
            supplier_id: $('select#supplier_id').val(),
            delivery_date: $('input#delivery_date').val()
        }
    })
        .done(pendingStocks => {
            console.log(pendingStocks);
            displayPendingStocks(pendingStocks);
        });
});