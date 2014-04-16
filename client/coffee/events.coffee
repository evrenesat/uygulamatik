# coffeescript'ten js'e derlemede console.log'larin sorunsuzca donusmesi icin gereken vasifsiz fonksiyon
foo = ->

    # sayfa hazir oldugunda
    #$(document).ready window.onDocReady
document.save_settings_stack = []
document.settings_save_in_process = false

$(document).bind('cache_filled', utils.loadLayoutCss)

$(window).bind 'uygulamatik_ready', () ->
    console.log "UYGULAMATIK READY!"
    if window.RESETDB
        persistence.reset()
    $(display).bind 'templates_fetched', ()->
        console.log "evnts do init jobs when templates_fetched"
        utils.loadAppCSS()
        udb.loadThemeCSS()
        Mnu.load_orders()
        Base.index()
        setInterval(udb.start_background_saver,7000)
        document['rld'] = udb.reset_db

    initDvice()
    udb.checkLocalDatabase()
    $('a.index_link').live 'click', (e) ->
        navigator.app.clearHistory()
#    console.log "cihaz surumu: #{device.version[0]}"
    showUp()
    document.addEventListener "backbutton", backbutton_handler, false
    $.get("images/buttonsag-h.png")
    $.get("images/buttonsol-h.png")
    if Dvice.vdigit < 4
        animelogo()
    else
        setInterval animelogo, 3000



    #    if document.alreadyready
    #        return
    #    document.alreadyready = true;
    $(window).resize () ->
        document.he = $(window).height()
        document.wi = $(window).width()
    $(window).trigger 'resize'

#    utils.loadLayoutCss()

    #    utils.devResMenu()
    #    $('ul.mainmenu li').css {height: "#{document.he * 9 / 100}px"}
    # eger sayfada hash (#) isareti yoksa sayfayi yeniler ve index'e gidilmesini saglar (gerekli mi?)
    if location.hash isnt ''
        location.hash = ''

#    display.fetchTemplate()
#    trans.startEngine()



    Base.scan_handler_views =
        'l': [Nav, Nav.show_location],
        'a': [Park, Park.show_wheels],
        't': [Mnu, Mnu.table_selected]



    # barcode tarama ekranına geçiş
#    $('#scan_barcode').live 'vmouseup', () ->
#        #        console.log 'Barcode Click'
#        window.plugins.barcodeScanner.scan ((result) ->
#            Base.qrscanner_handler result.text
#        ), ((err) ->
#            display.showMessage "Scan failed"
#        )

    # linklerle sayfa geçişi


    #        console.log document.nowloading
    #        if document.nowloading
    #            return

    #        if (command.indexOf '_do_') < 0
    #            document.nowloading = true
    #            setTimeout((()->document.nowloading = false), 1000)


    # form onaylama
#    $('form').live 'submit', (e) ->
#        e.stopImmediatePropagation()
#        e.preventDefault()
#        view = $(this).attr 'action'
#        data = display.urlToObj $(this).serialize()
#        display.callView view, data
#        return false


#    # ayarlamaları onaylayan butonların tıklanması (sayfa geçişi olmayan)
#    $('a.static_button').live 'vmouseover', (e) ->
#        #page = $(this).attr 'href'
#        page = $(this).data 'href'
#        views._sendData page, {}
#        e.stopImmediatePropagation()
#        e.preventDefault()


    # paylaşma olayı
    $('a.share_link').live 'vmouseup', (e) ->
        subject = $(this).data('subject')
        message = $(this).data('message')
        console.log "SHARE THIS #{subject} #{message}"
        window.plugins.share.show(
            subject: subject
            text: message
            () -> console.log 'Share basarili'
            () -> console.log 'Share hatali'
        )

    # hoverbuttonlarin basinca seçili olması
    $('a.hoverbutton, div.hoverbutton').live 'vmouseover', (e) ->
        $(this).addClass 'etkin'
        setTimeout((()=>$(this).removeClass 'etkin'), 300)

    # anamenüdeki tıklanın linklerin seçili olması
    $('ul.mainmenu li').live 'vmouseover', (e) ->
        $(this).addClass 'etkin'
        setTimeout((()=>$(this).removeClass 'etkin'), 400)

    $('a#gohome').live 'tap', (e) ->
        gotohome()

#    $('ul.mainmenu li').live 'tap', (e) ->
#        e.stopImmediatePropagation()
#        e.preventDefault()
#        command = $(this).find('a').data('href')
#        display.callView command

#    if !!~document.location.protocol.indexOf 'http'
##        utils.onWebClient()
#        showUp()

    $(window).on 'settingsOK', ()=>
        setEffect()

    if not window['downloadOnDemand']?
        window['downloadOnDemand'] = (obj)->
            src = $(obj).attr('src').split('/')
            imgsrc = src[src.length-1]
            ft = new FileTransfer()
            source = "#{settings.STATIC_SERVER_URL}media/uploads/#{imgsrc}"
            target = "#{settings.STORAGE_PATH}/#{imgsrc}"
            ft.download source, target,
            (()=>
                d = new Date();
                $(obj).attr("src", $(obj).attr("src")+"?td="+d.getTime())
            ),
            (()=>
                console.log "indirme basarisiz"
            )




#    $(window).on 'storageOk', ()=>
#        loadDefaults()


window.gotohome = ()->
    #    $('div.ui-page-active').removeClass('ui-page-active');
    #    $('div#index').addClass('ui-page-active').trigger('create')
    $.mobile.changePage '#index'
#    while jQuery.mobile.urlHistory.stack.length > 1
#        jQuery.mobile.urlHistory.stack.pop()
#    jQuery.mobile.urlHistory.activeIndex = 0


geri_git = (e) ->
    if e
        e.stopImmediatePropagation()
        e.preventDefault()
    console.log "geri gidiyoruz"
    document.backed = 1
    console.log "history length #{history.length}"
    if history.length == 1
        document.page_id = ''
        $.mobile.changePage "#index"
    if document.goto_home
        document.goto_home = false
        gotohome()
        #        document.location='index.html'
        #        window.history.go(1 - history.length)

        return

    #    if navigator.app?
    #        navigator.app.backHistory()
    #    else
    history.back()
    check_cleanup()


check_cleanup=->
    if document['cleanup']?
        document['cleanup']()




#animelogo = ()-> $("div#logor").fadeTo 1000, 0.99, ()-> if not document.page_id then $(this).fadeTo 1000, 0.2, animelogo
animelogo = ()->
    $('div#logor').toggleClass 'gorunur'

$(document).bind 'pageinit', (ev, options) ->
    page_id = ev.target.id
    console.log "on pageinit #{page_id}"
    document.page_id = page_id
    document.ee = ev
    #    $("##{page_id} #header").trigger("create")
    #    console.log "search this? #{Um.search_this}"
    setTimeout (()=>display.afterRenderJobs(page_id)), 0

$(document).bind 'pagechange', (ev, options) ->
    #    document.evv = ev
    page_id = ev.currentTarget.URL.split('#')[1]
    if page_id and page_id.indexOf '&' > -1
        page_id = page_id.split('&')[0]

    #    Um.shade.removeClass('on')


    document.page_id = page_id

    if document.backed? and document.backed == 1
        display.current_template = document.page_id
        document.backed = 0


    if page_id and '/' not in page_id
        geridugme = $("##{page_id} a.geriDugmesi")
        if geridugme
            geridugme.on 'vclick', geri_git

    check_cleanup()
    console.log "page changed to #{document.page_id}"
    #    if Um.auto_callview
    #        udb.setit('last_view', Um.auto_callview[0])
    #        udb.setit('last_params', Um.auto_callview[1] or '')

    #    console.log ev
    #    if document.page_id
    #        $("#geri").live 'vmouseover',  (e) ->
    #            e.stopImmediatePropagation()
    #            e.preventDefault()
    #            try
    #                navigator.app.backHistory()
    #            catch err
    #                console.log "back error #{err}"
    #            if document.cleanup
    #                document.cleanup()
    #                document.cleanup = null


    $('a.generic_button').on 'vmouseover', (e) ->
        $(this).addClass 'etkin'
        setTimeout (()=>$(this).removeClass 'etkin'), 400

    $('.ui-btn').on 'vmouseover', (e) ->
        $(this).addClass 'ui-btn-down-a'
        setTimeout (()=>$(this).removeClass 'ui-btn-down-a'), 400



showUp = () ->
    try
        navigator.splashscreen.hide()
    catch e
        console.log e.message
    #    $.mobile.listview.prototype.options.dividerTheme = "a";
    #    $.mobile.selectmenu.prototype.options.nativeMenu = false;
    #    $.mobile.defaultDialogTransition = udb.getit("transefekt")


    $("#index").addClass("thm-#{document.theme}")
    #    setTimeout "$('#hider').addClass('gorunur')",1000
    $('#hider').addClass('gorunur')
    $('#logolar').addClass('gorunur')
    $("#index").focus().trigger("click")


#    goToTestScreen()
#    Um.chart_flag()


setEffect = ()->
#    efekt_opasiti= if udb.getit("transefekt") == 'none' then 1 else 0
#    console.log "efekt #{udb.getit("transefekt")}"
#    $('head').append("<style>.ui-page-active{opacity:#{efekt_opasiti};}</style>")



backbutton_handler = (e)->
    e.preventDefault()


    console.log "backbutton page_id : #{document.page_id}"
    #    console.log prompt("Uygulamadan çıkılsın?")
    #    document.backed = 1
    console.log "back docid #{document.page_id}"
    if not document.page_id and confirm("Uygulamadan çıkılsın mı?")
        console.log "exiting..."
#        udb.setit('last_view', '')
#        udb.setit('last_params', '')
        navigator.app.exitApp()
    geri_git()



##    console.log document.cleanup
#    if document.cleanup
#        document.cleanup()
#        document.cleanup = null
##$.ready () ->
initDvice = ()->
    if $(window).height() < 100
        setTimeout ()=>
            initDvice()
        , 800
    else
        Dvice.init()




