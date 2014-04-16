trans =
    DEFAULT_LANG_OK: true
    DATA :
        messages:
            "":
                domain: "messages"
                lang: "en"
                plural_forms: "nplurals=2; plural=(n != 1);"
    MISSING_KEYS: []
    SELECTED_LANG: navigator.language.substr(0, 2)
    SAVE_REQUIRED: false #eger dil dosyasini sunucudan indirdiysek diske kaydetmeliyiz.


    t:(text,var1,var2)->
    tt:->
    startEngine: () ->
        console.log "TRNS start translation engine"
        console.log "OHAAAAAAAAA"
        trans.SAVE_REQUIRED = false
        trans.SELECTED_LANG = udb.getit('selected_lang') || navigator.language.substr(0, 2)
        trans.DEFAULT_LANG_OK = udb.getit('lang') == trans.SELECTED_LANG
        if not trans.DEFAULT_LANG_OK
            console.log "TRNS  default lang  is NOT ok"
            if trans.SELECTED_LANG in udb.getit('avail_langs')
                trans.loadTranslationData()
            else
                console.log "TRNS we are not supporting #{trans.SELECTED_LANG} lang."
                trans.setTranslator(trans.DATA)
        else
            console.log "TRNS DEFAULT IS OK."
            trans.setTranslator(trans.DATA)






    loadTranslationData: ()->
        console.log "TRNS  loadTranslationData."
#        debugger
        udb.getRecords(trans.SELECTED_LANG)
        trans.loadFromLocalWWW() #fail path >> loadFromStorage >> loadFromServer >>  ultimate fail!!!

    loadFromLocalWWW: () ->
        $.ajax(
            url: "js/gettext_#{trans.SELECTED_LANG}.js",
            dataType: 'json',
            success: trans.setTranslator
            error: trans.loadFromStorage
        )

    loadFromStorage: () =>
        console.log "TRNS  loadFromStorage."
        $.ajax(
            url: "#{settings.STORAGE_PATH}/gettext_#{trans.SELECTED_LANG}.js",
            dataType: 'json',
            success: trans.setTranslator
            error: trans.loadFromServer
        )

    loadFromServer: ()=>
        console.log "TRNS  loadFromServer."
        trans.SAVE_REQUIRED = true
        $.ajax(
            url: "#{settings.SERVER_URL}gettext/#{trans.SELECTED_LANG}/",
            dataType: 'json',
            success: trans.setTranslator
            error: trans.loaderror
        )

    loaderror:(e)->
        console.log "Load error #{e}"
        console.log e

    missing_key_handler: (key)->
        if trans.DEFAULT_LANG_OK or trans.SELECTED_LANG not in udb.getit('avail_langs')
            return
        if key not in trans.MISSING_KEYS
            trans.MISSING_KEYS.push(key)
#        console.log "Missing translation key #{key}"

    send_missing_keys: ()->
        console.log "trans.send_missing_keys"
        if trans.MISSING_KEYS.length
            url = settings.SERVER_URL + 'settext/' + trans.SELECTED_LANG + '/'
            $.post url, {keys: JSON.stringify(trans.MISSING_KEYS)}, (rdata)=>
                console.log "server response #{rdata}"
        else console.log "no missing keys"


    saveData: (data)->
        if trans.SAVE_REQUIRED
            udb.writer("gettext_#{trans.SELECTED_LANG}.js", data)

    setTranslator: (data) ->
        # Based on Jed (js gettext implementation)
        # http://slexaxton.github.com/Jed/
        gettext = new Jed(
            missing_key_callback: (key)=>
                trans.missing_key_handler(key)
            locale_data: data
            domain: 'messages'
        )
        trans.saveData(data)


        trans.t = ()->
            #eger cogulluk durumuna gore farkli metin gerekmiyorsa bu kullanabilir. cogu zaman bu isimizi gorur.
            #kullanimi
            #{{#_t("Aşağıdaki ogeleri sil")}}
            #{{#_t("Aşağıdaki %d adet ögeyi sil", adet)}}
            if arguments.length == 1
                return gettext.translate(arguments[0]).fetch()
            else
                args = [].slice.call(arguments)
                return gettext.translate(args.shift()).fetch(args)

        trans.tt = ()->


            #eger cogul degisken varsa
            #kullanimi:
            #{{#_tt("Aşağıdaki %d ögeyi sil","Aşağıdaki %d adet ögenin tümünü sil", adet)}}
            #{{#_tt("Aşağıdaki %1$s  ögeden %2$s adedi secildi","Aşağıdaki %1$s adet ögenin %2$s adedi secildi", adet, adet2)}}
            #TODO: girdide %d varsa, ceviride de olmak zorundami diye TEST etmek gerek
            args = [].slice.call(arguments)
            return gettext.translate(args.shift()).ifPlural(args.shift()).fetch(args)
        $(display).bind 'templates_fetched', trans.send_missing_keys
        display.fetchTemplate()


$(window).bind 'settingsOK', ()->trans.startEngine()
