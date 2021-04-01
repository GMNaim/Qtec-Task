$(document).ready(function () {
    // Hiding the ajax loader
    $("#ajax_loader").hide();
    // Checked/Unchecked checkbox and getting the filter items
    $(".form-check-input, #filter_date").on('click', function () {
        let filtered_items_object = {};

        // Filter according to custom date
        let from_date = new Date($("#from_date").val());
        let to_date = new Date($("#to_date").val());

        if (($("#from_date").val() !== '' && $("#to_date").val() === '') ||
            ($("#from_date").val() === '' && $("#to_date").val() !== '')) {
            alert('Please Select both date field');
        } else {
            if (from_date > to_date) {
                alert('Start date must be less than end date');
            } else if (from_date >= Date.now()) {
                alert('Start date must be less than today');
            } else if($("#from_date").val() !== '' && $("#to_date").val() !== ''){
                filtered_items_object.from_date = from_date.toISOString().split('T')[0];
                filtered_items_object.to_date = to_date.toISOString().split('T')[0];
            }
        }

        // Filtering checkbox inputs
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

        // Send AJAX GET request
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
