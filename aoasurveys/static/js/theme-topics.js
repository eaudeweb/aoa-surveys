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
