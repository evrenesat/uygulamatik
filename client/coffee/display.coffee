display =
    current_template: ''
    search_this: false
    divide_this: false
    render_callback: false
    templates:{}



    fetchTemplate: ->
        # tüm şablonu çeker, parcalar boler, derler, onbellekler
#        if document.on_the_web
#            settings.TEMPLATES_PATH = "#{STATIC_SERVER_URL}apppackages/#{settings.APPID}/#{settings.TEMPLATES_PATH}"
        $.get settings.TEMPLATES_PATH, (data) =>
            window['t'] = trans.t
            window['tv'] = udb.cache

            if document.on_the_web
                re = new RegExp settings.STORAGE_PATH, "g"
                data = data.replace re, settings.STORAGE_PATH
                console.log "templates prerendered for the web"
            templates = data.split('[[--]]')
            for tpl in templates
                te = tpl.split('+|+')
#                console.log("compiling template: #{t[0]}")
                if te[1]?
                    display.templates[te[0]] = doT.template(te[1])
            $(display).trigger('templates_fetched')
#            udb.setit('TEST','TESTDATATEST')
            console.log('templates_fetched')


    urlToObj: (url) ->
        obj = {}
        url.replace new RegExp("([^?=&]+)(=([^&]*))?", "g"), ($0, $1, $2, $3) -> obj[$1] = $3
        delete obj[prop] for  prop in obj when obj.hasOwnProperty prop and obj[ prop ] == ''
        obj


    back_to_home: (label) ->
        if label
            $('.geriDugmesi a').html label
        document.goto_home = true

    complete_button_action: (fn, label) ->
        if not label then label = 'Kaydet'
        console.log "complete button label : #{label}"
        $(aP+"#rightkontrol > div").html("<a data-icon='check'  data-role='button'>#{label}</a>").
        trigger('create').find('a').on 'click', ()=>
            fn()
            $('#rightkontrol a').remove()


    # gelen bilgilerle yeni sayfayı oluşturur
    renderPage: (data=null, callback, that) ->
        if Paginator.watcher_watcher
            clearInterval Paginator.watcher_watcher
            Paginator.stopScrollWatch()
        new_page = true
        force_new_page = false
        page_id = display.current_template
        display.render_callback = callback
        display.that = that or views #TODO FIX this hard coded 'views' shit!!!
        console.log "renderpage id : #{page_id} data:", data


        pagechange_options = {}
        if data
            if data['samepage']
                new_page = false
                delete data['samepage']
            if data['pagechange_options']
                pagechange_options = data['pagechange_options']
                delete data['pagechange_options']
            if data['page_id']
                page_id = data['page_id']
                delete data['page_id']
            if data['page_title']
                display.set_title = data['page_title']
                delete data['page_title']
            if data['template']
                page_id = data['template']
                template = data['template']
                delete data['template']
            if data['data']
                data = data['data']
            display.search_this = data.search_action?
            display.divide_this = data.listview?
        else
            data = {}
        data['tv'] = udb.cache
        data['t'] = trans.t
        data['assert'] = utils.assert
        data['fdate'] = utils.format_date

        console.log "renderPage final pageid: #{page_id} new_page: #{new_page} "

        temp = display.templates[template](data)


        if new_page
#            $('div.ui-page-active').hide('fast')
            existing = $('div#' + page_id)
            #            console.log "existence", existing
#            if existing.length and force_new_page
#                console.log "WE NEED FORCE NEW"
#                existing.removeClass('ui-page-active')
            if existing.length
                new_page = not existing.hasClass 'ui-page-active'
                console.log "hala yenimi", new_page
        if new_page or force_new_page
#            display.shade.addClass('on')
            if existing and not force_new_page
                existing.remove()
            if existing and force_new_page
                $("##{document.page_id} div.tmpl_wrapper").html($(temp).find(".tmpl_wrapper")).trigger("create")
            $(document.body).append temp
#            console.log("ABOOOOOO", temp)
            $.mobile.changePage "##{page_id}", pagechange_options
        else
#            $.mobile.navigate(page_id + '_' + udb.get_random())
            $("##{document.page_id} div.tmpl_wrapper").html($(temp).find(".tmpl_wrapper")).trigger("create")
            display.afterRenderJobs(page_id)
#        $("div[data-role='footer']").css({'position':'relative'})
#        setTimeout("$(\"div[data-role='footer']\").css({'position':'relative'})", 500)
#        setTimeout("$(\"div[data-role='footer']\").css({'position':'fixed'})", 1000)

    afterRenderJobs: (page_id)->
        if not page_id
            return
        $("div##{page_id}").addClass('superactive')
        $("div##{page_id} .tmpl_wrapper").addClass('tridi')
        setTimeout (()->$("div##{page_id}").removeClass('tridi')),1000
        if display.search_this
            display.insert_search(page_id)
            display.search_this = false
        if display.set_title
            $("div.superactive .ui-title").html(display.set_title)
            display.set_title = false
        if display.divide_this
            display.divide_list(page_id)
            display.divide_this = false
        if display.render_callback
            display.render_callback(display.that)
            display.render_callback = false


    showKeyboard:->
        try
            window.cordova.plugins.SoftKeyBoard.show()
        catch e
            console.log e.message

    showLoadingMessage: (msg = 'Yükleniyor', autohide_timeout = 0) ->
        setTimeout ()=>
            $.mobile.loading 'hide'
            $.mobile.loading 'show', theme: document.theme, text: msg, textVisible: true
            if autohide_timeout then setTimeout (()=>$.mobile.loading 'hide'), autohide_timeout
        ,0

    showMessage: (msg, auto = true, html = '') ->
        if msg
            msg = trans.t(msg)
        @showMessageBase msg, auto, html

    showMessageBase: (msg, auto = true, html = '') ->
        console.log msg
        $.mobile.loading 'hide'
        $.mobile.loading 'show', 'theme': document.theme, 'textVisible': true,
        'textonly': true, 'text': msg, 'html': html
        if auto
            timeout = if typeof auto == "number"  then auto else 4000
            setTimeout (()=>$.mobile.loading 'hide'), timeout

    insert_search: (page_id)->
        searchButton = $("div##{page_id} .searchbutton")
        if searchButton.hasClass('searchOK')
            return
        console.log "search for #{page_id}"
        searchButton.addClass('searchOK')
        searchButton.on 'vmouseup', (e)=>
            e.stopPropagation()
            e.preventDefault()

            search_div = $("div##{page_id} div.searchPopup").css(display: 'block')

            setTimeout (()=>
                $("div##{page_id} #keyword").focus()
                display.showKeyboard()
            ), 300
            search_div.find('#dosearch').on "click", ()=>
                e.stopPropagation()
                e.preventDefault()
                keyword = search_div.find('#keyword').val()
                action = search_div.find('#action').val()
                if not action
                    action = page_id
                console.log "search action #{action}"
                if not keyword
                    display.showMessage 'Lütfen arama kriterinizi giriniz'
                else
                    #FIXME : categori filtresini yoksayarak yapiliyor
                    #                    display.["search_#{action}"](keyword)
#                    display.callView action, keyword
                    search_div.hide()
            search_div.find('button#closesearch').on 'click', (e)->
                e.stopPropagation()
                e.preventDefault()
                search_div.hide()


    divide_list: (page_id)->
        selector = $("##{page_id} ul.lstvw")
        console.log "divide it #{page_id}"
        if selector.length
            selector.parent().addClass('pedli')
            if selector.filter('.ui-listview').length then selector.listview('refresh') else selector.listview ({autodividers: true,
            autodividersSelector: (li)->
                html=$(li).find('h3').html()
                return if html then html.substring(0, 1) else ''
            })




#
#
#    # verilen linkten json tipinde veri döndürür
#    callView: (view, params) ->
#        # callview aldigi parametereleri onislemden geicrip ilgili view'i cagirir
#        # cagirilan view mevcut degilse, ayni isimde bir template oldugu varsayimiyla "arguments" ile renderPage'i cagirir
#        #
#        #view                                                     > display.view()
#        #view?kw_a=1                                                 > display.view({a:1})
#        #view?a=1                                                 > display.view(1)
#        #view?a=1&b=2                                             > display.view({a:1,b:2})
#        #view           params = 1                                > display.view(1)
#        #view           params = { keyword: 'str', catid:1 }      > display.view({keyword:'str',catid:1})
#        #view?a=1       params = { keyword: 'str', catid:1 }      > display.view(1, {keyword:'str',catid:1})
#        #view?a=1&b=2   params = 1                                > display.view({a:1,b:2}, 1)
#        #view?a=1&b=2   params = 'keyword'                        > display.view({a:1,b:2}, 'keyword')
#        #view?a=1&b=2   params = { keyword: 'str', catid:1 }      > display.view({a:1,b:2,keyword:'str',catid:1})
#        #view?a=1&b=2   params = { keyword: 'str', catid:1 }      > display.view({a:1,b:2,keyword:'str',catid:1})
##        display.auto_callview = [view, params]
#
#        view = view.replace '#', ''
#
#        #        just_one_url_param=null
#        just_one_param=null
#        url_params = null
#        if '?' in view
#            [view, url_params] = view.split '?'
#            url_params = display.urlToObj url_params
#        #        console.log "url_params",url_params
#        display.current_template = view.replace('.','_')
#
##        base_module = BASEVIEWS
##        console.log(display.)
#        if view.indexOf('.')>0
#            _views = view.split('.')
#            base_module = views[_views[0]]
#            view = base_module[_views[1]]
#        else if views.BASE[view]
#                base_module = views.BASE
#                view = base_module[view]
#        else
#            view = ()=> display.renderPage(arguments)
#
#
#        if not (url_params or params)
#            return view.call(base_module)
#
#        if url_params
#            url_keys = Object.keys(url_params)
#            if url_keys.length == 1
#                key = url_keys[0]
#                if key.substring(0, 3) isnt 'kw_'
#                    just_one_url_param = url_params[key]
#                else
#                    val = url_params[key]
#                    key = key.substring(3)
#                    url_params = {}
#                    url_params[key] = val
#
#
#        if typeof(params) is "object" and Object.keys(params).length == 1 and (just_one_url_param or not url_params)
#            just_one_param = params[Object.keys(params)[0]]
#
#        if url_params and params
#            if typeof just_one_url_param isnt "undefined"
#                view.call base_module, just_one_url_param, just_one_param or params
#            else
#                view.call base_module, $.extend url_params, params
#        else if url_params
#            view.call base_module, (if typeof just_one_url_param isnt "undefined" then just_one_url_param else url_params)
#        else
#            view.call base_module, params

