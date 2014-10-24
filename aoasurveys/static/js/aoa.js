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
      var slugs = [];
      $('#selected tr td:first-child').each(function() {
          slugs.push($(this).text());
      });
      var data = $(this).serializeArray();
      data.push({name: "slugs", value: slugs});

      $.post(url, data, function(resp) {
          if (resp.success == true) {
              $('.alert').show();
          }
      }, "json");
    });

    $('.multiplechoicefield').parents('ul').each(function() {
      var items = $(this).children();
      if (items.length >= 10) {
        items.children().children().addClass('multichoicewidget');
      }
    });

    $('.multichoicewidget').parents('li').hide();
    $('.multichoicewidget').parents('ul').each(function() {
      var select = $('<select>').attr('class', 'multichoice')
      $(this).children().children().each(function() {
        select.append($('<option>')
          .attr('value', $(this).attr('for'))
          .text($.trim($(this).text())));
      });
      $(this).before(select);
    });

    $('select.multichoice').on('change', function() {
      var id = $(this).children(':selected').val();
      var label = $("label[for='" + id + "']");
      label.children().prop('checked', true);
      label.parent().show();
    });

    $('.multichoicewidget').on('change', function() {
      if (!$(this).is(':selected')) {
        $(this).parents('li').hide();
      }
    });
});
