X=
    # magaza, urunler ve kampanyalar icin ana kategorileri getirir
    main_categories: (cat)->
        udb.vars.product_category.all().filter('upper_category', '=', null).list (result) =>
            magazmi_katilimcimi = if udb.getit('type') == '10' then 'Mağazalar' else 'Katılımcılar'
            switch cat
                when 'products' then title = trans.t 'Ürünler'
                when 'places' then title = trans.t magazmi_katilimcimi
                when 'campaigns' then title = trans.t 'Kampanyalar'
            display.renderPage categories: result, page: cat, search_action: cat, page_title: title ()->
                if result.length == 0
                    display.showMessage "Kayıt bulunamadı!"
                $('#listview_button').on "click", ()=>
                    display.callView cat


    places: (catid, keyword)->
        persistence.debug = true
        console.log "STORES args", catid, keyword
        if typeof catid is "object"
            paginate = catid.paginate
            select_for_feedback = catid.select_for_feedback
            keyword = catid['keyword'] or keyword
            catid = catid['catid']
        else if isNaN catid
            keyword = catid

        query = udb.vars.place.all().filter('type', '=', 1).or(new persistence.PropertyFilter('type', '=', 20)).limit(settings.record_per_page)
        context =
            search_action: "places?catid=#{catid}",
            'catid': catid,
            'keyword': keyword,
            select_for_feedback: select_for_feedback or false
        #        console.log "context", context
        #        console.log "catid", Boolean(catid), catid
        if (not isNaN catid) and catid > 0
            query = query.filter('category_id', '=', parseInt(catid))
        if keyword
            query = query.filter('name', 'like', "%#{keyword}%")

        display.renderPage context, ()->
            Paginator.init query: query, object_name: 'places', context: context


    fastfood_place: (place_id) ->
        udb.vars.place.findBy 'place_id', place_id, (s) =>
            udb.vars.store_product_category.all().filter('place', '=', s.id).list (categories) =>
                display.renderPage categories: categories, place: s, ()->
                    for c in categories
                        console.log 'categorys'
                        console.log c
                        c.products.list (products) =>
                            if products.length
                                console.log products

                                prlen = products.length
                                box_total = (document.wi / 4) * prlen
                                margins = prlen * 3
                                satir = $("div#sff_product_#{products[0].place_category_id}")
                                #                                console.log satir
                                #                                console.log products[0]
                                satir.css(width: "#{box_total + margins}px").html(display.templates._fastfood_place_boxes products)
                                that = this
                                satir.find('> div').on 'click', (e) ->
                                    that.callView "product_details?id=#{$(this).data 'pid'}"
                                iScrollFood.scrollThis products[0].place_category_id,'s'
    #                                    satir.on 'vmousedown', ()=>
    #                                        $('.fastplacetitle').removeClass('etkin')
    #                                        $("#lid#{products[0].place_id} a").addClass('etkin')






    fastfood_wellcome: ->
        display.renderPage {},()->
            $('#showfastfoods').click ()=>
                display.callView 'fastfooders', 'passwellcome'
            $('#dontwellcomeagain #cbx').change ()=>
                udb.setit 'fastfood_nowellcome', 1
                display.callView 'fastfooders', 'passwellcome'

    fastfooders: (keyword)->
        show_wellcome = not udb.getit 'fastfood_nowellcome'
        if keyword == 'passwellcome'
            show_wellcome = false
            keyword = ''
        if show_wellcome
            return display.callView 'fastfood_wellcome'

        context =
            search_action: 'fastfooders'
        udb.vars.place.all().filter('type', '=', 20).order('name').list (foods) =>
            context.foodplaces = foods
            display.renderPage context, ()->
                iScrollFood.init()
                @_append_fastfoods(foods, keyword)



    _append_fastfoods: (fastfooders, keyword)->
        #        template = doT.template(@templates['_fastfood_boxes'])
        for s in fastfooders
            q = udb.vars.product.all().prefetch('place').filter('place', '=', parseInt(s.id)).filter('showcase', '=', 1)

            if keyword then q = q.filter('name', 'like', "%#{keyword}%")
            #            console.log q
            q.list (products) =>
                document.d = products
                if products.length
                    prlen = products.length
                    kutu = (document.wi / 4)
                    place = products[0].place
                    context = products: products, place: place
                    #                    console.log(place)
                    box_total = kutu * prlen + (kutu * 1.5 )
                    margins = (prlen + 1) * 3
                    satir = $("#ff_product_#{products[0].place_id}")
                    satir.css(width: "#{box_total + margins}px").html(display.templates._fastfood_boxes context)
                    that = this
                    satir.find('> div').on 'click', (e) ->
                        that.callView "product_details?id=#{$(this).data 'pid'}"

                    satir.find('> a').on 'click', (e) ->
                        that.callView "fastfood_place?id=#{$(this).data 'placeid'}"

                    satir.on 'vmousedown', ()=>
                        $('#fastfoods .fast_title').removeClass('etkin')
                        $("#lid#{products[0].place_id}").addClass('etkin')
                    iScrollFood.scrollThis products[0].place_id

        if keyword
            #sonuc icermeyen magazalari temizliyoruz
            setTimeout (()->
                $("#fastfoods .fast_product_container").each ->
                    unless ($(this).find("div")).length
                        $(this).parent().prev().remove()
                        $(this).parent().remove()
            ), 1200
    #FIXME: settimeout sadece workaround. asenkron listelemenin bittigini anlamanin bi yolunu bulmaliyiz!!




#
#
#
#        _set_back: (text)->
#    #        $.mobile.page.prototype.options.backBtnText = text
#
#        friends: [
#            {name: 'Aylin Kahraman', avatar: 'g1.png', id: 1}
#            {name: 'Mert Gündüz', avatar: 'b1.png', id: 2}
#            {name: 'Ceren Falin', avatar: 'g2.png', id: 3}
#            {name: 'Fatih Akıncı', avatar: 'b2.png', id: 4}
#            {name: 'Aslı Balta', avatar: 'g3.png', id: 5}
#            {name: 'Ayşe Çelik', avatar: 'g4.png', id: 6}
#            {name: 'Cem Derin', avatar: 'b3.png', id: 7}
#            {name: 'Turgut Atik', avatar: 'b4.png', id: 8}
#            {name: 'Tuğçe Birkan', avatar: 'g5.png', id: 9}
#            {name: 'Su Selin Özkan', avatar: 'g6.png', id: 10}
#            {name: 'Elvin Melvin', avatar: 'g7.png', id: 11}
#            {name: 'Mert Durmuş', avatar: 'b5.png', id: 12}
#            {name: 'Tan Çağlayan', avatar: 'b6.png', id: 13}
#        ]
#
#        _get_selected_friends: ()->
#            $("#allfriends input:checked").map(()->@value).get()
#
#        nerde:
#            1: "mağazada"
#            20: "restoranda"
#            30: "WC"
#            40: "kavşağında"
#            50: "kapısında"
#            60: "park yerinde"
#
#
#        meethere: (id)->
#            arkadas_sayisi = udb.getit('meetfriends').length
#            udb.setit 'nav_from', id
#            if arkadas_sayisi
#                udb.vars.place.findBy 'place_id', id, (s) =>
#                    display.showMessage "Seçtiğiniz #{arkadas_sayisi} kişiye şuanda #{s.name} adlı #{@nerde[s.type]} olduğunuzu bildirdik.", 6000
#            else
#                display.callView 'meetpoint'
#
#        meetpoint_friends: ()->
#            selected_friends = udb.getit 'meetfriends'
#
#            if selected_friends
#                $(@friends).map(()->
#                    if selected_friends.indexOf("#{@.id}") > -1
#                        @.selected = true
#                ).get()
#
#
#            display.renderPage friends: @friends, type: 'all',()->
#                $("#meetfriends input[type='checkbox']").live 'change', (e)=>
#                    console.log "w1"
#                    if not e.target.checked
#                        console.log "#allcheckbox-#{$(e.target).data('id')}"
#                        cb = $(e.target)
#                        $("#allcheckbox-#{cb.data('id')}").attr('checked', false)
#                        cb.parents("div.ui-checkbox").hide('fast', ()->$(@).remove())
#                        $("#meetpoint_friends input[type='checkbox']").checkboxradio("refresh")
#
#                $("#allfriends input[type='checkbox']").on 'change', (e)=>
#                    #        console.log "hmmmmmm #{e.target.checked} #{e.target.value}"
#                    display.complete_button_action (()=>
#                        udb.setit 'meetfriends', @_get_selected_friends()
#                        display.callView 'meetpoint_ok'
#                        display.back_to_home()
#                    ), 'Kaydet'
#
#
#                $("#show_meetfriends").click ()=>
#                    meetgroup = @friends.filter((e)=>@_get_selected_friends().indexOf("#{e.id}") > -1)
#                    $("#meetfriends").html(display.templates._meetpoint_friendlist checkall: true, type: 'meet', friends: meetgroup).trigger('create')
#
#                    $('#allfriends').hide()
#                    $('#meetfriendswrapper').show()
#
#                $("#show_allfriends").click ()->
#                    $('#allfriends').show()
#                    $('#meetfriendswrapper').hide()

    #      meetpoint_ok: ()->
    #        renderPage {}, ()=>
    #


    place_details: (id)->
        udb.vars.place.findBy 'place_id', parseInt(id), (s) =>
            if s is null then display.showMessage 'Kayıt bulunamadı'
            else
                s.campaigns.order('start_date', false).prefetch('product').one (c) =>
                    if c?
                        c.s_date = utils.format_date(c.start_date)
                        c.e_date = utils.format_date(c.end_date)
                        s.campaign = c
                    display.renderPage template: s.template, data: s
                    $("#place_details .ui-title").html(s.name)


    place_campaigns: (place_id) ->
        udb.vars.place.findBy 'place_id', place_id, (place) =>
            place.campaigns.order('campaign_id', false).list (campaigns) =>
                if not campaigns.length
                    return display.showMessage "Bu mağzaya ait kampanya kaydı bulunamadı."
                display.renderPage 'place': place, 'campaigns': campaigns



    place_products: (place_id) ->
        udb.vars.place.findBy 'place_id', place_id, (place) =>
            place.products.order('name').list (products) =>
                if not products.length
                    return display.showMessage "Bu mağzaya ait ürün kaydı bulunamadı."
                display.renderPage listview: 1, 'place': place, 'products': products
    #                , ()=>



    place_discounts: (place_id) ->
        udb.vars.place.findBy 'place_id', place_id, (place) =>
            place.products.filter('cut_price', '>', 0).order('product_id', false).list (products) =>
                if not products.length
                    return display.showMessage "Bu mağzaya ait indirimli ürün bulunamadı."
                display.renderPage listview: 1, 'place': place, 'products': products


    about_us: (place_id)  ->
        udb.vars.place.findBy 'place_id', place_id, (s) =>
            display.renderPage data: s

    # ürün detayları
    product_details: (id)->
        console.log "product_id #{id}"
        #        persistence.debug = true
        if not isNaN(id) then id = parseInt(id)
        udb.vars.product.all().filter((if isNaN(id) then "id" else "product_id"), '=', id).prefetch('place').one (p) =>
            if p is null
                display.showMessage 'Kayıt bulunamadı'
            else
                udb.vars.place.findBy 'place_id', p.place_id, (s) =>
                    p.place = s
                    display.renderPage p
                    $('a#urun_sayi_artir').on 'click', () ->
                        count = $('input[name=count]').val()
                        $('input[name=count]').attr 'value', parseInt(count) + 1
                    $('a#urun_sayi_azalt').on 'click', () ->
                        count = $('input[name=count]').val()
                        if parseInt(count) > 1 then $('input[name=count]').attr 'value', parseInt(count) - 1

    last_page: 0
    last_keyword: ''
    total_records: 0
    record_per_page: 40



    products: (catid, keyword)->
        #        persistence.debug = true
        console.log "products args", catid, keyword
        if typeof catid is "object"
            paginate = catid.paginate
            keyword = catid['keyword'] or keyword
            catid = catid['catid']
        else if isNaN catid
            keyword = catid

        query = udb.vars.product.all().prefetch('place').order('name').limit(settings.record_per_page)
        context = search_action: "products?catid=#{catid}", 'catid': catid, 'keyword': keyword
#        if keyword
#            context.samepage = 1

        if parseInt(catid) > 0
            query = query.filter('category_id', '=', parseInt(catid))
        if keyword
            query = query.filter('name', 'like', "%#{keyword}%")

        display.renderPage context, ()->
            Paginator.init query: query, object_name: 'products', context: context



    campaigns: (catid, keyword)->
        #        persistence.debug = true
        #        console.log "products args", catid, keyword
        if typeof catid is "object"
            paginate = catid.paginate
            keyword = catid['keyword'] or keyword
            catid = catid['catid']
        else if isNaN catid
            keyword = catid

        #        console.log "products catid:", catid, keyword
        query = udb.vars.campaign.all().prefetch('place').order('end_date').limit(@record_per_page)
        context = search_action: "campaigns?catid=#{catid}", 'catid': catid, 'keyword': keyword
        #        console.log "context", context
        #        console.log "catid", Boolean(catid), catid
        if parseInt(catid) > 0
            query = query.filter('category_id', '=', catid)
        if keyword
            query = query.filter('name', 'like', "%#{keyword}%")

        if paginate
            return @paginator query, 'campaigns'

        @last_page = 1
        display.renderPage context, ()->
            Paginator.loading()

            Paginator.init query: query, object_name: 'campaigns', context: context

    #        query.list (results)=>
    #            if not results.length
    #                display.showMessage "Kriterlere uyan ürün kaydı bulunamadı"
    #            else
    #                context.campaigns = results
    #                display.renderPage context, ()->
    #                    @clearIfNoMore(query)






    # kampanya detayları
    campaign_details: (campaign_id)->
        if not isNaN(campaign_id) then campaign_id = parseInt(campaign_id)
        udb.vars.campaign.all().filter((if isNaN(campaign_id) then "id" else "campaign_id"), '=', campaign_id).prefetch('place').prefetch('product').one (c) =>
            if c is null then display.showMessage 'Barkodla eşleşen kayıt bulunmamakta'
            else
                console.log c.start_date
                #                console.log c
                c.s_date = utils.format_date(c.start_date)
                c.e_date = utils.format_date(c.end_date)
                display.renderPage c



#        placecache:{}







    #    # feedback sayfası
    #

    feedback_simple:->
        @feedback_survey target_type:'host', target_name:udb.cache["name_short"]

    #feedback diye bir view yok, template implict olarak cagriliyor.
    feedback_select: (type, search_keyword)->
        if type == 'place'
            return display.callView 'places', select_for_feedback: true
        query = udb.vars[type].all()
        if search_keyword then query = query.filter('name', 'like', "%#{search_keyword}%")
        query.list (resultset) =>
            display.renderPage template: "feedback_select_#{type}", data:
                listview: 1
                items: resultset
                search_action: "feedback?type=#{type}"

    feedback_survey: (kwargs)->
        console.log kwargs
        if kwargs.mood
            @vars.feedback.mood = kwargs.mood
            display.callView "feedback_form"
        else
            if kwargs.type
                udb.vars[kwargs.type].all().filter('id', '=', kwargs.id).one (s)=>
                    @vars.feedback = target: s, type: kwargs.type
            else if kwargs.target_type
                @vars.feedback = type: kwargs.target_type, target: {name: kwargs.target_name}
            display.renderPage feedback: @vars.feedback, template: 'feedback_survey'

    feedback_form: ()->
        console.log "geri bildirim lazimmi #{@_is_personal_info_needed()}"
        if @_is_personal_info_needed()
            @vars.process = 'feedback_form'
            @set_personal tab: false, save_button_label: "Devam Et"
        else
            display.renderPage template:'feedback_form', feedback: @vars.feedback, user_name: udb.getit 'name', ()=>
                $('textarea#feedback_send_message').focus()
                display.showKeyboard()
                $("textarea#feedback_send_message").one "keydown", ()=>
                    display.complete_button_action @send_feedback, 'Tamamla'


    send_feedback: ()->
        @vars.feedback.message = $('#feedback_send_message').val()
        fb = @vars.feedback

        data =
            customer : JSON.stringify @get_personal_info()
            oid : fb.target["#{fb.type}_id"]
            content_type: fb.type
            type: fb.mood
            msg: fb.message
#        console.log data
        display.showLoadingMessage("Gönderiliyor...")
        $.post settings.SERVER_URL + 'save_feedback/', data, (rdata)=>
#            $.mobile.loading 'hide'
            display.renderPage template: 'feedback_thankyou'
            display.back_to_home()






    # tarama sonuclari
    scan_handler_views:
        'p': @product_details, 's': @place_details, 'c': @campaign_details, 'l': @show_location, 'a': @parkasist

    qrscanner_handler: (arr) ->
        if arr.indexOf('http://') > -1
            arr = arr.split('/')[3]
        cat = arr.substring(0, 1)
        id = arr.substring(1)
        console.log "SCANNER RESULTS:: #{cat}, #{id}"
        if @scan_handler_views[cat]?
            @scan_handler_views[cat] id
        else
            display.showMessage 'Karekod tanınamadı'


    # sepeti goster
    basket: ->
        udb.vars.chart.all().prefetch('product').list (result) =>
            if result.length
                sepet = []
                for r in result
                    if r.product isnt null
                        record = 'name': r.product.name, 'id': r.id, 'image': r.product.image, 'count': r.count
                        if r.product.cut_price then record['price'] = r.product.cut_price * r.count else record['price'] = r.product.price * r.count
                        sepet.push record
                display.renderPage products: sepet, ()->
                    display.complete_button_action ()=> display.callView 'complete_shopping',
                    "Siparişi Tamamla"
                    $('#basket .deletebutton').on 'click', (e)=>
                        @_do_delete_from_chart($(e.target).parents('.deletebutton').data 'sid')

            else
                display.showMessage 'Sepetiniz boş'



    # sepetten urun silme
    _do_delete_from_chart: (id)->
        console.log id
        udb.vars.chart.findBy 'id', id, (c) =>
            persistence.remove c
            $('#basket #tr_' + id).hide('slow')
            @chart_flag()


    # urunu sepete ekleme
    add_to_chart: (args)->
        console.log 'Add to chart'
        udb.vars.chart.findBy 'product_id', args.product_id, (p) =>
            if p isnt null
                p.count = args.count
                persistence.add p
                persistence.flush ()=>
                    display.showMessage "", true, "<center><img src='images/basketfull.png' /> <br>#{args.count} adet #{p.name} sepetinize eklendi. </center>"
            else
                c = new udb.vars.chart count: args.count, product_id: args.product_id
                udb.vars.product.findBy 'product_id', args.product_id, (p) =>
                    c.product = p
                    persistence.add c
                    persistence.flush ()=>
                        display.showMessage "", true, "<center><img src='images/basketfull.png' /> <br>#{args.count} adet #{p.name} sepetinize eklendi. </center>"
            @chart_flag()
            display.callView 'basket'

    #sepette urun varsa farkli ikon goster
    chart_flag: ->
        udb.vars.chart.all().count (sayi)=>
            console.log "sepetteki urun sayisi #{sayi}"
            if sayi then $('a#show_basket').addClass 'dolu' else $('a#show_basket').removeClass 'dolu'


    facebook_connect: ->
        display.showMessage 'Facebook ile bağlanma işlevi çok yakında tamamlanacaktır.'



    # kisisel ayarlar sayfasi
    save_personal_settings: (args)->
        udb.setit 'name', decodeURIComponent(args.name).replace(/\+/g, " ")
        udb.setit 'email', decodeURIComponent(args.email).replace(/\+/g, " ")
        udb.setit 'tel', decodeURIComponent(args.tel).replace(/\+/g, " ")
        udb.setit 'address', decodeURIComponent(args.address).replace(/\+/g, " ")

        console.log "process", @vars.process
        if @vars.process
            setTimeout ()=>
                if @vars.process is 'checkout' then display.callView 'set_payment'
                else display.callView @vars.process
            ,100

        else
            display.showMessage 'Güncelleme Başarılı'


    # magaza guncelleme
    update_places: ->
        if navigator.network.connection.type isnt Connection.NONE then udb.versionComparison true
        else display.showMessage 'İnternet bağlantısı yok!!!'

    # ayarlar sayfasi
    settings_page: ->
        display.renderPage {}, ()->
            display.callView "_is_personal_info_needed", 1
            $('.ui-fixed-hidden').removeClass('ui-fixed-hidden')

    get_personal_info:->
        return {
            name: udb.getit 'name'
            email: udb.getit 'email'
            tel: udb.getit 'tel'
            address: udb.getit 'address'}

    set_personal: (args)->
        if args
            in_tab = true
            if args.save_button_label
                save_button_label= args.save_button_label
                in_tab = args.tab
        else
            [save_button_label, in_tab] = ['', '']

        s =
            data: @get_personal_info()
            template : 'set_personal'
        if in_tab
            s.samepage = 1


        display.renderPage s, ()->
            $("##{document.page_id} input:first").focus()
            $("##{document.page_id} input,textarea").one "keydown", ()=>
                display.complete_button_action ()=>$("##{document.page_id} form").submit(),
                save_button_label





    # odeme seceneklerini getiren sayfa
    set_payment: (tab) ->
        display.renderPage if tab then samepage: 1 else null



    settings: ->
        info = utils.getDevInfo()
        context =
            samepage: 1
            data:
                efekt: udb.getit('transefekt', '')
                theme: udb.getit('defaulttheme', 'c')


        console.log info

        display.renderPage context, ()->
            $("#effect").change ()=>
                efkt = $("#effect").val()
                udb.setit("transefekt", efkt)
                display.showMessage "Geçiş efekti '#{efkt or 'varsayılan'}' olarak ayarlandı."
                setTimeout (()=>document.location = "index.html"),1000



            $("#downloadimages").click ()=>
                $("#downloadimages").addClass('ui-disabled')
                udb.justImages()



    setTheme:(theme)->
        thms = {'a':'Gece', 'c':'Gündüz'}
        udb.setit("defaulttheme", theme)
        display.showMessage "Tema '#{thms[theme]}' olarak ayarlandı."
        setTimeout (()=>udb.writeDefaultJS()),500
        setTimeout (()=>document.location = "index.html"),1000

    about_app: ->
        info = utils.getDevInfo()
        context =
            samepage: 1
            data:
                info: info,
                devpower: Dvice.power
                devcaps: Dvice.caps
                devdigit: Dvice.vdigit
        display.renderPage context, ()->


            $("#resetdb").click ()=>

                udb.deleteAllTables ()=>
                        @cache = {}
                        display.showMessage "Veritabanı sıfırlandı."
                        setTimeout (()=>document.location = "index.html"),1000

            $("#devpower").change ()=>
                Dvice.power = $("#devpower").val()
                display.showMessage "Dvice.power #{Dvice.power} olarak ayarlandi"
            $("#devcaps").change ()=>
                Dvice.caps = $("#devcaps").val()
                display.showMessage "Dvice.caps #{Dvice.caps} olarak ayarlandi"
            $("#devdigit").change ()=>
                Dvice.vdigit = $("#devdigit").val()
                display.showMessage "Dvice.vdigit #{Dvice.vdigit} olarak ayarlandi"

#            $("#resetsettings").click ()=>
#                udb.vars.dbsettings.all().destroyAll ()=>
#                    @cache = {}
#                    display.showMessage "Ayarlar sıfırlandı."
            if Dvice.caps < 2
                    $("#devinfo").css height:'auto'

#            $("#debug").click ()=>
#                $('head').append '<script src="http://debug.phonegap.com/target/target-script-min.js#fbornva"></script>'
#                display.showMessage "Debugger attached"


    # secilen odeme seceneginin veritabanina kaydi
    payment_info_save: (args)->
        udb.setit 'payment_type', args.payment_type
        if @vars.process is 'checkout'
            display.callView 'shop_summary'
        else
            display.showMessage 'Ödeme yöntemi kaydedildi'

    # alisveris ozeti
    shop_summary: ->
        udb.vars.chart.all().prefetch('product').list (results) =>
            items = []
            for r in results
                record = {'product__name': r.product.name, 'count': r.count}
                if r.product.cut_price then record['price'] = r.product.cut_price * r.count else record['price'] = r.product.price * r.count
                items.push record
            sum = 0
            sum += parseFloat i.price for i in items
            display.renderPage 'items': items, 'sum': sum

    # alisverisi sonlandirma
    complete_shopping: ->
        @vars.process = 'checkout'
        if @_is_personal_info_needed()
            display.callView 'set_personal', tab: 0, save_button_label: 'Ödeme Yöntemi Seç'
        else
            display.callView 'set_payment'

    _is_personal_info_needed: ->
        return not (udb.getit('name') and udb.getit('address') and udb.getit('email')? and udb.getit('tel'))


    # alisveris tamamlama sonrasi ekrani
    shopping_result: ->
        udb.vars.chart.all().prefetch('product').list (results) =>
            items = []
            for r in results
                record = {'product': r.product.product_id, 'count': r.count}
                if r.product.cut_price then record['price'] = r.product.cut_price * r.count else record['price'] = r.product.price * r.count
                items.push record
            sum = 0
            for i in items
                sum += parseFloat i.price
            data =
                items: JSON.stringify items
                sum:sum
                customer : JSON.stringify @get_personal_info()
                payment_metod: udb.getit 'payment_type'
            $.post settings.SERVER_URL + 'save_order/', data, (rdata)=>
                udb.vars.chart.all().destroyAll () =>
                    app_time = (Math.floor Math.random() * 27) + 3
                    display.renderPage order_no: rdata.order_id, app_time: app_time, ()->
                        display.back_to_home()
