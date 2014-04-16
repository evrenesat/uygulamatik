$(document).ready(function () {
    function sort_fields() {
        var fields = $("input.vIntegerField").filter("[id$='-sort'],[id$='-order']");
        for (var i= 0, _len=fields.length; i<_len; i++) {
            var row = i%2 ? 'row2' : 'row1';
            $(fields[i]).val(i+1).parents('tr').attr('class', row);
        }
    }
    var fixHelper = function(e, ui) {
        ui.children().each(function() {
            $(this).width($(this).width());
            $(this).height($(this).height());
        });
        return ui;
    };

    var sortable_fields = $("input.vIntegerField").filter("[id$='-sort'],[id$='-order']");
    if (sortable_fields.length) {

        sortable_fields.parent().css({width:'40px'});
        var width = sortable_fields.parent().css({'text-align':'center'});
        sortable_fields.css({'display':'none'})
        sortable_fields.after('<img src="/media/images/sort_icon.png" class="sorthandle" />');

        $('table#result_list tbody, div.inline-group table tbody').sortable({
            update: function () {
                sort_fields();
                if ($('td.original').length) {
                    $('td.original').next().css({'padding':'2em 0 1em 0.5em'});
                    $('div.inline-group table tbody tr#moduleselection_set-empty').addClass('empty-form');
                }
            },
//            delay: 300,
            handle: ".sorthandle",
//            distance: 15,
            helper: fixHelper
        });
    }

});
