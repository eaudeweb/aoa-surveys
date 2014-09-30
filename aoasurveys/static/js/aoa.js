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

$(function () {
    $('body').on('click', '.launch-modal', function () {
        var url = $(this).data('action');
        var title = $(this).data('title');
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.modal-body').html(data);
                $('h4.modal-title').html(title);
                $('#add-modal-submit').data('action', url)
            },
            error: function (data) {
                alert('Error launching the modal')
            }
        })
    });
});
