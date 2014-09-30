$(function () {
    $('#advanced-filtering-button').on('click',function (evt) {
        evt.preventDefault();
        var form = $('#advanced-filtering-form');
        var active = $(this).data('active');
        var activate = 'Advanced filtering';
        var deactivate = 'Hide advanced filtering';
        if (active) {
            $(this).data('active', false);
            $(this).text(activate);
            form.hide();
        } else {
            $(this).data('active', true);
            $(this).text(deactivate);
            form.show();
        }
    }).click();
});
