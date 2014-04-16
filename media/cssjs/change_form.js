$(document).ready(function () {

    $('div.inline-related tr.add-row a').live('click', function () {
        parent.mainframe.load();
    });


    // ceviri alanlarinda dillerin ayarlanmasi
    var translation_wrapper = $('div#translations-group');
    if (translation_wrapper.length) {
        var select_fields = $('select[id$="lang"]');
        for (var i=0,_lens=select_fields.length; i<_lens; i++) {
            var val = i+1;
            var lang = $($(select_fields[i]).find('option')[val]).text();
            $(select_fields[i]).prop('selectedIndex', val).after('<h2>'+lang+'</h2>');
        }
        $('select[id$="lang"], a[id$="lang"]').css('display', 'none');
    }

    // verileri kaydederken ekleme yapilmamis dil cevirilerinin es gecilmesi
    if (translation_wrapper.length) {
        $('form').submit(function (e) {
//            e.preventDefault();
            var button = $(this);

            var divs = $('div#translations-group div.inline-related');
            for (var j=0,_length=divs.length; j<_length; j++) {
                var skip = true;
                var required_fields = $(divs[j]).find('label.required').siblings('input, select');
                var lang_field = null;
                for (var k=0,_l=required_fields.length; k<_l; k++) {
                    var item = $(required_fields[k]);
                    var id = item.attr('id');
                    id = id.substring(id.length - 4);
                    if (id == 'lang') lang_field = item;
                    else {
                        if (item.val()) skip = false;
                    }
                }
                if (skip) lang_field.val('');
            }
            return true;

//            button.parents('form').submit();
        });
    }

    // dosya yukleme gorselligi
    var upload_fields = $('div.fileupload input');
    upload_fields.change(function () {
        $(this).parent().addClass('uploaded');
    });

    $('span.clearable-file-input input').click(function () {
        if ($(this).attr('checked')) {
            $(this).parent().siblings('img').css({'opacity':'0.25'});
        } else {
            $(this).parent().siblings('img').css({'opacity':'1'});
        }
    });


    // tabular inline icin ckeditor gizleme
    $('tr.add-row a').live('click', function () {
        $('div.tabular textarea').css({'visibility':'visible', 'display':'block'});
        $('div.tabular span[id^=cke_id]').remove();
    });

    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.on('instanceReady', function () {
            $('div.tabular textarea').css({'visibility':'visible', 'display':'block'});
            $('div.tabular span[id^=cke_id]').remove();
        });
    }


});

