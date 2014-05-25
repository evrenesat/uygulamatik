Evnt=
    render : (data=null, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)

    spn_list: ()->
        if udb.cache["sponsors"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            @render  {'template':'Spn_list', 'data': udb.cache["sponsortypes"]}, ()=>
                @bind cB, @spn_detail


    spn_detail:(id)->
        @render 'template': 'Spn_detail', 'data': udb.cache["sponsors"][id]




    dlg_list: ()->
        if udb.cache["delegates"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            @render {'template':'Dlg_list', 'delegates':udb.cache["delegates"]}, ()=>
                @bind cB, @dlg_detail

    dlg_detail:(id)->
        @render 'template': 'Dlg_detail', 'data': udb.cache["delegates"][id]



    favorite_exhibitors: ->
        context =   'favorite_exhibitors': udb.cache["favexhibitors"],
        'template':'Ex_favorites',
        'samepage': true,
        'page_title':trans.t('Favori Katılımcılar')
        @render context, ()=>
            @bind cB, @exh_detail



    favorite_files: ->
        if  (not udb.cache["favexhibitorfiles"] or not udb.cache["favexhibitorfiles"].length)
            display.showMessage 'Favorileriniz boş'
            return
        context =   'favorite_files': udb.cache["favexhibitorfiles"],
        'template':'Ex_file_favorites',
        'samepage': true,
        'page_title':trans.t('Belgelerim')
        @render context, ()=>
            @bind cB1, @favs_file_addremove
            @bind cB, @open_file


    exhibitors: ()->
        if not (udb.cache["exhibitors"]["none"]? and udb.cache["exhibitors"]["none"])
            @render {'template': 'Ex_list', 'exhibitors': udb.cache["exhibitors"]}, ()=>
                @bind cB, @exh_detail
        else
            display.showMessage 'Kayıt bulunamadı'


    exh_detail:(id)->
        exhib = udb.cache["exhibitors"][id]
        console.log "EXH"
        console.log exhib
        exhib['favorites_enabled'] = 'Evf' in udb.module_names
        exhib['files_enabled'] = 'Exl' in udb.module_names
        exhib['infavorites'] = exhib['id'] in udb.cache["favexhibitors"]
        exhib['template'] = 'Ex_detail'
        @render exhib, ()=>
            ibb = @bind iB0, ()->
                $('div#exhibitor_detail_pane > div').hide ()->$('div#exhibitor_description').show('normal')
#            ibb.trigger('click')
            @bind iB1, ()->
                $('div#exhibitor_detail_pane > div').hide ()->$('div#exhibitor_files').show('normal')

            @bind iB2, @favs_remove
            @bind iB3,  @favs_add
            $(iB4).click ()-> Nav.show_location(utils.gotid(@), true)


            @bind cB, @open_file
            @bind cB1, @favs_file_addremove
#            $("div[data-role='footer']").css({'position':'absolute'})



    open_file:(id) ->
        if confirm(trans.t("%s dosyası indirilecek, onaylıyor musunuz", udb.cache["exhibitorfiles"][id].title))
            utils.open_external_url("#{settings.STATIC_SERVER_URL}media/uploads/#{udb.cache["exhibitorfiles"][id].file}")

    favs_remove:(id, btn)->
        favs = udb.getit('favexhibitors', [])
        favs.splice(favs.indexOf(id),1)
        udb.setit('favexhibitors', favs)
        $(btn).hide().siblings().show()
        display.showMessage('Katılımcı favorilerinizden çıkarıldı')

    favs_add:(id, btn)->
        favs = udb.getit('favexhibitors', [])
        favs.push id
        udb.setit('favexhibitors', favs)
        $(btn).hide().siblings().show()
        display.showMessage('Katılımcı favorilerinize eklendi')

    favs_file_addremove:(id)->
        favs = udb.getit('favexhibitorfiles', [])
        if id in favs
            favs.splice(favs.indexOf(id),1)
            display.showMessage('Dosya favorilerinizden çıkarıldı.')
            $('#exflfav'+id).hide('normal')
        else
            favs.push(id)
            display.showMessage('Dosya favorilerinize eklendi.')
        udb.setit('favexhibitorfiles', favs)



    event_list: ->
        if udb.cache["events"] is []
            display.showMessage 'Kayıt bulunamadı'
        else
            events = []
            @render {'template':'Evnt_list', 'events': udb.cache["events"]}, ()=>
                @bind cB, @event_detail


    favorite_list: ()->
        data = count:
            'events' : udb.cache["favevents"].length
            'files' : udb.cache["favexhibitorfiles"].length
            'exhibitors' : udb.cache["favexhibitors"].length

        @render template:'favorite_list', data: data, ()=>
            @bind iB1, ()=>@favorites @favorite_events
            @bind iB2, ()=>@favorites @favorite_exhibitors
            @bind iB3, ()=>@favorites @favorite_files



    favorites: (cb)->
        @render template:'favorites', ()=>
            @bind iB1, @favorite_events
            @bind iB2, @favorite_exhibitors
            @bind iB3, @favorite_files
            cb.call(@)


    favorite_events: ->
        if  (not udb.cache["favevents"] or not udb.cache["favevents"].length)
            display.showMessage 'Favorileriniz boş'
            return
        favevents = []
        for day in udb.cache["events"]
            dayevents = []
            for event in day[1]
                if event.id in udb.cache["favevents"]
                    event.didx = udb.cache["events"].indexOf(day)
                    event.idx=day[1].indexOf(event)
                    dayevents.push(event)
            if dayevents.length
                favevents.push([day[0],dayevents])
        console.log favevents
        context = 'events': favevents, 'template':'Evnt_list', 'samepage': true, 'page_title': trans.t('Etkinliklerim')
        @render context, ()=>
            @bind cB, @event_detail




    event_detail:(date_idx, a)->
#            date_idx = parseInt(kw.date_idx)
        event_idx = $(a).data('idx')
        event = udb.cache["events"][date_idx][1][event_idx]
        event['date_idx'] = date_idx
        event['infavorites'] = event.id in udb.cache["favevents"]
        event['favorites_enabled'] = 'Evf' in udb.module_names
        event['speakers_enabled'] = 'Evs' in udb.module_names
        event['template'] = 'Evnt_detail'
        @render event, ()=>
            $(iB0).click ()-> Nav.show_location(utils.gotid(@), true)
            @bind iB1, @event_description
            @bind iB2, @list_speakers
            @bind cB, @show_speaker
            @bind iB4, @remove_event_from_favs
            @bind iB5, @add_event_to_favs


    speakers: ->
        if not udb.cache["events"].length
            display.showMessage 'Kayıt bulunamadı'
        else
            speakers = (udb.cache["speakers"][keys] for keys in Object.keys(udb.cache["speakers"]))
            @render {'template':'Evnt_speakers', 'speakers': speakers}, ()=>
                @bind cB, @show_speaker

    description:->
        $('div#event_detail_pane > div').hide ()->$('div#event_description').show('normal')

    show_speaker:(id)->
        @render 'template':'Evnt_speaker', data:udb.cache["speakers"][id]


    list_speakers:->
        $('div#event_detail_pane > div').hide ()->$('div#event_speakers').show('normal')

    remove_event_from_favs:(id)->
        favs = udb.getit('favevents', [])
        favs.splice(favs.indexOf(id),1)
        udb.setit('favevents', favs)
#        display.callView 'event_favorites'
        display.showMessage('Etkinlik favorilerinizden çıkarıldı')

    add_event_to_favs:(id)->
        favs = udb.getit('favevents', [])
        favs.push id
        udb.setit('favevents', favs)
        display.showMessage('Etkinlik favorilerinize eklendi')
