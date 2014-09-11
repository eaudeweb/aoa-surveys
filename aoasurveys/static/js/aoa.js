$(function () {
    $('#advanced-filtering-button').on('click', function(evt) {
        evt.preventDefault();
        var form = $('#advanced-filtering-form');
        var activate = 'Advanced filtering'
        var deactivate = 'Hide advanced filtering'
        switch ($(this).text()) {
            case activate:
                $(this).text(deactivate);
                form.show();
                break;
            case deactivate:
                $(this).text(activate);
                form.hide();
                break;
        }
    });
});

$(function () {
    var topics = [
        'w_green-economy-topics', 'w_water-resources-topics',
        'w_water-resource-management-topics', 'w_resource-efficiency-topics',
    ]
    $("select[name$='w_theme']").on('change', function(evt) {
        $(this).children().each(function() {
            var selector = "select[name$='" + topics[$(this).val()] + "']"
            var row = $(selector).parents('tr')
            if ($(this).is(':selected')) {
                row.show()
            }
            else {
                row.hide()
            }
        });
    }).change();
});
