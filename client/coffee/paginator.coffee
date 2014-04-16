Paginator =
    context:
        {}
    object_name: ''
    last_page: 0
    #    current_page:0
    #    last_pos:0
    list_div: ''
    query: null
    total_records: 0
    per_page: 0 #40
    max_records: 150
    li_height: 100
    watching: false
    window_height: 0
    near_bottom: 0
    watcher_watcher: 0
    lastScrollPosition: 0

    current_li_total: 0
    #
    #query
    #object_name
    #
    init: (args)->
        #        $.mobile.loading('show')
        Paginator.last_page = 0
        Paginator.window_height = $(window).height()
        Paginator.near_bottom = Paginator.window_height / 2
        Paginator.context = args.context or Paginator.context
        Paginator.total_records = 0
        Paginator.object_name = args.object_name
        Paginator.per_page = settings.record_per_page
        Paginator.query = args.query
        Paginator.list_div = $("ul##{Paginator.object_name}_list")
        Paginator.list_div.html('')
        #        Paginator.list_div.css backgroundColor:'black'
        #        console.log "paginator", args, Paginator.last_page, skip_these
        console.log "perpage #{Paginator.per_page}"
        Paginator.bottomHandler()
#        if not Paginator.watcher_watcher
#            Paginator.watcher_watcher = setInterval ()=>
#                Paginator.watchScroll()
#            , 2000


    #<editor-fold desc="falanca">
    #        Paginator.watcher_watcher = setInterval ()=>
    #            console.log "wawa #{$(window).scrollTop()}, #{Paginator.lastScrollPosition}"
    #            lastpos = Paginator.lastScrollPosition
    #            Paginator.lastScrollPosition = $(window).scrollTop()
    #            if lastpos == Paginator.lastScrollPosition
    #                Paginator.checkScroll()
    #        ,2000

    #                $('#tmpul').remove()
    #                ul.append(html)
    #                if Paginator.total_records <= Paginator.record_per_page * Paginator.last_page
    #                    $('div.ui-page-active #morebutton').remove()


    #                Paginator.scrollUpdate
    #                    bottom_callback:()=>
    #                        args.page =
    #                        Paginator.paginator args


    #                console.log html
    #.parent().listview('refresh')
    #                console.log $('body').scrollTop(), $('body').scrollTop() - (document.he/5)
    #                $('body').scrollTop($('body').scrollTop() + (document.he * 0.9 ))
    #</editor-fold>


    noResults: ->
        display.showMessage "Kayıt bulunamadı!"

    cleanUp: (prepend)->
        uls = Paginator.list_div.find('li')
        if Paginator.current_li_total > Paginator.max_records
            clear = uls.length - Paginator.max_records
            console.log "cleanup #{clear}"
            if prepend
                uls.slice(0 - clear).remove()
            else
                uls.slice(0, clear).remove()
            Paginator.current_li_total = Paginator.max_records
    #$('html,body').animate scrollTop: $(window).scrollTop() - (Paginator.li_height * clear)
    #FIXME: tepedeki kayitlari silince kayma oluşuyor. bunu çözmeliyiz.
    #FIXME: tepedeki kayıtları silince en başa "<< geri" tuşu koymak gerek.

    #
    #results: db results
    #insert_method: append or prepend
    #
    updatePageList: (args)->
        #        console.log "upl ul leng",  Paginator.list_div.find('ul').length
        #        $.map args.results, (r)=>$.get("#{Um.settings.STORAGE_PATH}pr_s_#{r.image}")
        Paginator.context[Paginator.object_name] = args.results
        Paginator.current_li_total += args.results.length
        Paginator.context.page = Paginator.last_page
        Paginator.list_div[args.insert_method](display.templates["_#{Paginator.object_name}_listbox"] Paginator.context)
        #        console.log "upl ul 2 leng",  Paginator.list_div.find('li').length
        #        setTimeout ()=>
        #        if args.insert_method == 'prepend'
        #            $('html,body').animate scrollTop: Paginator.li_height * args.results.length
        #        else if $(window).scrollTop() + Paginator.window_height >= $(document).height -200
        #            $('html,body').animate {scrollTop: $(window).scrollTop()+ Paginator.li_height}, 800
        $.mobile.loading('hide')
        Paginator.watchScroll()
        Paginator.cleanUp()
    #        ,1000


    loading: ->
        $.mobile.loading('show', text: "Yükleniyor...", textVisible: true)

    calculateTotal: ->
        Paginator.query.count (total)=>
            console.log "total", total
            Paginator.total_records = total
        Paginator.li_height = Paginator.list_div.find('li:first').height()


    bottomHandler: ->
        console.log "bottomhandler page #{Paginator.last_page} total_records #{Paginator.total_records}"
        skip_these =  Paginator.per_page * Paginator.last_page
        #        console.log "skip", skip_these, "lastp", Paginator.last_page
        console.log "total records #{Paginator.total_records}"
        if not Paginator.total_records or (Paginator.last_page * Paginator.per_page) < Paginator.total_records
            display.showLoadingMessage()
            console.log "YUKLENIYOR LAN!!!"
            Paginator.query.skip(skip_these).list (results)=>
                if results.length
                    console.log results
                    Paginator.updatePageList results: results, insert_method: 'append'
                    Paginator.last_page += 1
                    if not Paginator.total_records
                        Paginator.calculateTotal()
                else
                    Paginator.noResults()
            #                    Paginator.watchScroll()
        else
            if not Paginator.total_records
                Paginator.noResults()
    #            else
    ##                setTimeout ()=>
    #                Paginator.watchScroll()
    ##                ,500


    topHandler: ->
        if Paginator.last_page >= 0
            $.mobile.loading('show')
            skip_these =  Paginator.per_page * Paginator.last_page
            #            console.log "skip", skip_these, "lastp", Paginator.last_page
            Paginator.query.skip(skip_these).list (results)=>
                Paginator.updatePageList results: results, insert_method: 'prepend'
                Paginator.last_page = Paginator.last_page - 1
        else
            setTimeout ()=>
                #                Paginator.watchScroll()
                $.mobile.loading('hide')
            , 500


    stopScrollWatch: ->
        Paginator.watching = false
        $(window).unbind('scroll')


    watchScroll: ()->
        console.log "pageid" + document.page_id + "  " + Paginator.object_name
        if not Paginator.watching and document.page_id == Paginator.object_name
            #            Paginator.watching=true
            Paginator.checkScroll()
            setTimeout ()=>
                $(window).scroll ()=>Paginator.checkScroll()
            , 1000


    checkScroll: ->
        #<editor-fold desc="topevents">
        #        console.log "btRq: #{$(window).scrollTop() + Paginator.window_height >= $(document).height() * 0.85} tpRq: #{$(window).scrollTop() < 200}"
        #        if  not $(window).scrollTop()
        #            Paginator.stopScrollWatch()
        #            console.log "TOPev"
        #            Paginator.topHandler()
        #        else
        lastpos = Paginator.lastScrollPosition
        Paginator.lastScrollPosition = $(window).scrollTop()
#        console.log "checkscroll #{lastpos} != #{Paginator.lastScrollPosition}"
        if $(window).scrollTop() + Paginator.window_height >= ($(document).height() * 0.80) and lastpos != Paginator.lastScrollPosition
            Paginator.stopScrollWatch()
            console.log "BTOMevBTOMevBTOMevBTOMevBTOMev scrolltop: #{$(window).scrollTop()}"
            Paginator.bottomHandler()

#</editor-fold>
