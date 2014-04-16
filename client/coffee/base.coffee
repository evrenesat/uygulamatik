Base=
    ###
    Anasayfayi dolduran nesne
    ###
#    index_div : $('#index')
    index:->
        @index_div = $('#index')
        @set_background()
        @set_header()
        @set_module_icons()
        @show_optional_icons()
        $(cB).on 'tap', (e) ->
            e.stopImmediatePropagation()
            e.preventDefault()
            mdl = start_points[$(this).data('fn')]
            mdl[1].call(mdl[0], $(this).data('oid'))

    set_background:->
        if udb.cache["background_image"]
            $('div#mainheader').css({backgroundImage:"url(#{udb.cache["static"]}/#{udb.cache["background_image"]})"})
            bg = "url(#{udb.cache["static"]}/#{udb.cache["background_image"]})"
            console.log "BG #{bg}"
            if udb.getit('app_bg') and Dvice.caps > 1
                css = "body>div.ui-page-active {background: #{bg};}"
                utils.loadCSS(css)
            else
                @index_div.css({'background':bg})


    set_header:->
        header_type = udb.cache["header_type"] or 'space'
        @index_div.append(display.templates["_header_#{header_type}"]({}))

    set_module_icons:->
        if udb.cache["modules"]?
            @index_div.find('div#icons').remove()
#            console.log display.templates['_mainmenu'](udb.cache["modules"])
            @index_div.append(display.templates['_mainmenu'](udb.cache["modules"]))

    show_optional_icons:->
        if Mnu.order_count
            $('#show_kafe_cart').css({'display':'block'}).click ()-> Mnu.show_order()
        if udb.getit('show_qrcode_button')
            $('#scan_barcode').css({'display':'block'}).click ()-> Base.scan_qrcode()


    scan_qrcode:->
        window.plugins.barcodeScanner.scan ((result) ->
            Base.qrscanner_handler result.text
        ), ((err) ->
            display.showMessage "Scan failed"
        )


    scan_handler_views: {}
        #will filled after uygulamatik be ready

    qrscanner_handler: (arr, cat) ->
        console.log "SCANNER RESULTS:: #{arr}"
        if arr.indexOf('http://') > -1
            arr = arr.split('/')[3]
        if isNaN(parseInt(arr))
            cat = arr.substring(0, 1)
            id = arr.substring(1)
        else
            id = arr
        if cat and id and @scan_handler_views[cat]?
            @scan_handler_views[cat][1].call(@scan_handler_views[cat][0], id)
        else
            display.showMessage 'QRCode not recognized'



