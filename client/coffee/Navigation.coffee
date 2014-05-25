Nav=
    #Basit haritalar ve Noktadan Noktaya Navigasyon (NNN)
    render : (data=null, callback)-> display.renderPage(data, callback, Nav)
    bind : (query, callback)-> utils.bind(query, callback, Nav)

    myScroll : null
    save_iscroll:''
    target_offset:100
    scroll_last_x:0
    scroll_last_y:0
    touch_start_x:0
    touch_start_y:0
    offset:0
    squares : []
    nodes : []
    setpoints: ->
        ###
        NNN baslangic ve bitis noktalarinin secimi
        ###
        to = udb.getit('nav_to')
        from = udb.getit('nav_from')
        context =
            'listview': 1,
            'template':'Nav_setpoints',
            'nodes': udb.cache["coordinates"]
            'to': if udb.cache["coordinates"][to]? then udb.cache["coordinates"][to].name else '',
            'from': if udb.cache["coordinates"][from]? then udb.cache["coordinates"][from].name else ''
        @render context, ()=>
            @bind iB0, @find_with_barcode
            @bind iB1, @show_location
            @bind cB, @set_from
            @bind cB1, @set_to


    set_from:(id)->
        @set_point('from', id)

    set_to:(id)->
        @set_point('to', id)

    set_point:(wht, id)->
        udb.setit "nav_#{wht}", id
        $("#nav_#{wht}_container").trigger('collapse').find("span.nav_title").html udb.cache["coordinates"][id].name
        if udb.getit 'nav_from' and udb.getit 'nav_to'
            $(iB1).addClass 'ui-btn-active'



    find_with_barcode:->
        ###
        NNN baslangic noktasini karekodla sec
        ###
        window.plugins.barcodeScanner.scan ((result) ->
            display.showMessage 'Start point selected.'
            arr = result.text
            #FIXME : urun yada kampanyaysa ilgili magzayi bulmamiz gerek.
            if arr.indexOf('http://') > -1
                arr = arr.split('/')[3]
            cat = arr.substring(0, 1)
            id = arr.substring(1)
            if cat=='c' or cat=='p'
                return display.showMessage 'Please scan a parking or place qrcode.'
            console.log "qrcode nav_from #{id}"
            udb.setit 'nav_from', id
            setTimeout (()->@setpoints()), 500
        ), ((err) ->
            display.showMessage 'Uygun sonuç bulunamadı'
        )


    show_location: (to, pointer=false) ->
        ###
        NNN harita goster
        ###
        if typeof to is "object"
            from = to.from
            to = to.to
        if isNaN to
            to = udb.getit 'nav_to'
        from = if pointer!=true and udb.cache['nav_from'] then udb.cache['nav_from'] else to

        console.log "from #{from} to #{to}"
        if from and to

            mapgraph = udb.getit 'mapgraph'
            #        debugger
            try
                paths = dijkstra.find_path(mapgraph, from, to)
            catch e
                if from != to
                    from = to
                    paths = dijkstra.find_path(mapgraph, from, to)
                console.log "DIJKSTRA ERROR ::", e
            document.paths = paths


            coordinates = udb.getit 'coordinates'
            style = ""
            map = udb.cache["maps"][coordinates[from]['map_id']]
            node_cords = []
            $.each paths, (index, path)->
#                    node_cords.push id: path, left: all_cords[path].x, top: all_cords[path].y
                console.log "SAME MAP", coordinates[from]['map_id'], coordinates[path]['map_id']
                if coordinates[from]['map_id'] == coordinates[path]['map_id']
                    node_cords.push 'id': path, 'left': coordinates[path]['x'], 'top': coordinates[path]['y']
            console.log "SHOWLOCATION, path nodes :: ", paths

            @render {'template':'show_location', 'map': map, 'nodes': node_cords, 'pagechange_options': {'transition': 'none'}},()=>
                $("#nd#{paths[0]}").addClass('startNode')
                $("#nd#{paths[(paths.length)-1]}").addClass('endNode')

                @add_scroller 'wrapper'
                @doNavigation paths, coordinates
                @touchToGoInit 'mapimg', map

                $(".startNode .endNode").each ()->
                    o = $(this)
                    o.css 'top', ( o.css 'top' - o.css 'height' )
                    o.css 'left', ( o.css 'left' - o.css 'width' )



    _connect_nodes: (paths)->
        ###
        haritada yolu ciz
        ###
        jsPlumb.Defaults.Connector = "Straight"
        jsPlumb.Defaults.Endpoints = [
             [ "Dot", radius: 1 ],
             [ "Dot", radius: 1 ]
        ]
        style = strokeStyle: "red", lineWidth: 5
        console.log "CONNECT_NODES :: path nodes", paths
        for path,i in paths
            if paths.length > i + 1
                #                console.log "connecting nd#{path} nd#{paths[i+1]}"
                try
                    jsPlumb.connect({source: "nd#{path}", target: "nd#{paths[i + 1]}", paintStyle: style})
                catch e
                    console.log "Error while connecting  nd#{path} to nd#{paths[i + 1]}"
                    #                    console.log e
                    throw e



    add_scroller: (divid) ->
        ###
        iscoll'u ilklendir. NNN ve basit haritada ortak kullanilir
        ###
        iscroll_opts =
            'bounce': false,
            'hScrollbar': false,
            'vScrollbar': false,
            'zoom': true,
            'zoomMin': 0.5,
            'zoomMax': 1,
            ###*@this {@myScroll}###
            'onScrollEnd':()->
                @scroll_last_x = Math.abs(@x)
                @scroll_last_y = Math.abs(@y)
            ###*@this {@myScroll}###
            'onZoomEnd': ()->
                m=$('#mapimg')
                console.log this.scale
                if this.scale > 0.8
                    m.addClass 'zoom'
                else
                    m.removeClass 'zoom'
        @myScroll = new iScroll(divid, iscroll_opts)
        preventer = (e) -> e.preventDefault()
        document.addEventListener('touchmove', preventer, false)
        document.cleanup = ()->
            try
                if @save_iscroll and document.page_id == @save_iscroll
                    return
                document.removeEventListener('touchmove', preventer, false);
                @myScroll.destroy();
                @myScroll = null;
                console.log "myscroll temizlendi"
                document.cleanup = null
            catch error
                console.log "err: #{error}"

        #        $('#show_location #container').css({width: document.wi, height: document.he})
        #        button_padding = parseInt(document.he * 0.02)
        #        $('#art').css({padding: button_padding}).on 'click', ()->
        #            if myScroll.scale < 2
        #                myScroll.zoom 1, 1, myScroll.scale+0.5
        #        $('#eks').css({padding: button_padding}).on 'click', ()->
        #            if myScroll.sc  ale > 0.5
        #                myScroll.zoom 1, 1, myScroll.scale-0.5

#            setTimeout (()->$.get("images/map.jpg")), 1000
#            console.log 'AddScroller', coords, paths

    doNavigation: (paths, coords) ->
        ###
        once hedefe gider, ardindan yolu cizdirir
        ###
        setTimeout (()=>
            @myScroll.refresh()
            default_zoom = 0.5
            @myScroll.zoom 1, 1, default_zoom
            n0 = coords[paths[0]]
            n1 = coords[paths[paths.length-1]]

            #onceden guzergahin ortasina scrol ediyorduk
            #x = ((n0.x + n1.x) / 2 - document.wi) * default_zoom
            #y = ((n0.y + n1.y) / 2 - document.he) * default_zoom

            #hedefe scroll edecegiz
            x = (n1.x - document.wi) * default_zoom
            y = (n1.y - document.he) * default_zoom

            @myScroll.scrollTo 0 - x, 0 - y
            #                console.log x,y
            #                console.log -x, -y
            @_connect_nodes paths

        ), 0

    list_maps: ()->
        if udb.cache["maps"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            @render  template:'Nav_list_maps', 'maps': udb.cache["maps"], ()=>
                @bind cB, @show_map

    show_map:(id)->
        @squares = []
        map = udb.cache["maps"][id]
        context = 'template':'Nav_show_map', 'map': map, 'pagechange_options': {'transition': 'none'}
        @render context, ()=>
            @add_scroller('wrapper_simple')
            @touchToGoInit('mapimg_simple', map)



    touchToGoInit:(divid,  map)->
        mapimg = $('#'+divid)
        if not @squares.length
            @target_offset = map['offset']
            @offset = mapimg.offset()['top']
            for nid in udb.cache["mapnodes"][map['id']]
                node = udb.cache["coordinates"][nid]
#                    console.log "node", udb.cache["mapnodes"][map['id']], node
                @nodes.push node
                @squares.push [node.x, node.y]
            console.log "Calculated Squares"
            console.log @squares
        mapimg.on 'touchstart',(e)=>@recordTouches(e)
        mapimg.on 'tap', (e)=>@processTouch(e)

    recordTouches: (e)->
        ###
        dokunma noktasini kaydet
        ###
        console.log "RECORD #{e.originalEvent.touches[0].pageX}"
        @touch_start_x= e.originalEvent.touches[0].pageX
        @touch_start_y= e.originalEvent.touches[0].pageY


    processTouch: (e)->
        ###
        dokunulan noktaya en cok map.offset kadar mesafede bir node varsa, o node'a gidiyoruz
        ###
        if  @touch_start_x and @myScroll.scale == 1
#                console.log n for n in @squares
            y = @scroll_last_y + @touch_start_y - @offset
            x = @scroll_last_x + @touch_start_x
            node = utils.nearest_point([x, y], @squares, @target_offset)
            if node >= 0
                @gotoNode node
                console.log "GOTO", node
                console.log x, y
            @touch_start_x = 0
            @touch_start_y = 0


    gotoNode: (node)->
        node = @nodes[node]
        if node['type'] == 10
            @save_iscroll = 'Ex_detail'
            Evnt.exh_detail udb.cache['node2exh'][node['id']]




