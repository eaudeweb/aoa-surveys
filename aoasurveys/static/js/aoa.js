$(function () {
    $('#advanced-filtering-button').on('click', function (evt) {
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
