$(document).ready(function () {
    // Hiding the ajax loader
    $("#ajax_loader").hide();

    // Checked/Unchecked checkbox and getting the filter items
    $(".form-check-input").on('click', function () {
        let filtered_items_object = {};
        $(".form-check-input").each(function (index, element) {
            // let filtered_item_value = $(this).val();
            let filtered_item_type = $(this).attr('data-filter');
            filtered_items_object[filtered_item_type] = Array.from(
                document.querySelectorAll(
                    'input[data-filter=' + filtered_item_type + ']:checked')
            ).map((element) => {
                return element.value;
            });
        });

        // Send data using AJAX
        $.ajax({
            url: '/filter-searches',
            data: filtered_items_object,
            dataType: 'json',
            beforeSend: () => {
                // Showing ajax loader
                $("#ajax_loader").show();
            },
            success: (response) => {
                // Hiding the ajax loader
                $("#ajax_loader").hide();

                // Showing/adding filtered response
                $("#search_items").html(response.data);

                // Setting the total row number of the search table
                let table = document.getElementById('searches_table');
                document.getElementById('total_row').innerText =
                    `Total Search${table.tBodies[0].rows.length > 1 ? 'es' : ''} (${table.tBodies[0].rows.length})`;

                // Showing message if no search is found after filter
                if (table.tBodies[0].rows.length === 0) {
                    table_body = document.getElementById('search_items');
                    table_body.innerHTML = '<tr style="text-align: center;">' +
                        '<td colspan="7">No Matching search</td></tr>';
                }
            }
        });

    });

});
