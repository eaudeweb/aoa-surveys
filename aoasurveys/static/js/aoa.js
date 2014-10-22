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

    $('#orderfields').on('submit', function (e) {
      e.preventDefault();
      var url = $(this).attr('action');
      var tab = $('.sub-header').attr('tab')
      var slugs = [];
      $('#selected tr td:first-child').each(function() {
          slugs.push($(this).text());
      });
      var data = $(this).serializeArray();
      data.push({name: "slugs", value: slugs});
      data.push({name: "tab", value: tab});

      $.post(url, data, function(resp) {
          if (resp.success == true) {
              $('.alert').show();
          }
      }, "json");
    });
});
