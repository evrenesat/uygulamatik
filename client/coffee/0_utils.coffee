utils =
    getDocSize : ()->
        docsize = "@doc_height:#{$(window).height()}px;@doc_width:#{$(window).width()}px;"

#        background_color_from_theme = $('#index').css('color').substring(4,7)
#        console.log "background_color_from_theme: #{background_color_from_theme}"
#        docsize += "@arkrnk:#{background_color_from_theme};"
#        docsize += "@arkrnk:0;"
        docsize += "@semitransbg:#{udb.getit('semitransbg','rgba(0,0,0, 0.60)')};"
        docsize += "@verytransbg:#{udb.getit('verytransbg','rgba(0,0,0, 0.30)')};"

#        docsize += "@arkrnk2:0;"
#        docsize += if document.theme == 'a' then '@arkrnk:255;' else '@arkrnk:255;'
#        docsize += if document.theme == 'a' then '@arkrnk2:0;' else '@arkrnk2:128;'
        docsize



    loadLayoutCss : () ->
        if $(window).height() < 300
            return setTimeout (()=>loadLayoutCss()), 400
        console.log "transef", udb.getit("transefekt")
        $.get "css/layout.less", (d)=>
            p = less.Parser()
            p.parse utils.getDocSize() + d, (e, tree) =>
                $('head').append("<style type='text/css'>#{tree.toCSS()}</style>")

    loadAppCSS : () ->
        if udb.cache["themecss"]?
            p = less.Parser()
            p.parse utils.getDocSize() + udb.cache["themecss"], (e, tree) =>
                $('head').append("<style type='text/css'>#{tree.toCSS()}</style>")


    loadCSS : (css) ->
        p = less.Parser()
        p.parse utils.getDocSize() + css, (e, tree) =>
            $('head').append("<style type='text/css'>#{tree.toCSS()}</style>")




    format_date: (date)->
        i = date.lastIndexOf '\:'
        t = date.substring(0, i).replace('T', ' ').replace(/-/g, '/')
        sd = new Date t
        sd_day = if sd.getUTCDate() < 10 then '0' + sd.getUTCDate() else sd.getUTCDate()
        sd_month = if sd.getUTCMonth() < 9 then '0' + (sd.getUTCMonth() + 1) else (sd.getUTCMonth() + 1)
        return sd_day + '/' + sd_month + '/' + sd.getUTCFullYear()

    getAppId : () ->
      return prompt("Lütfen uygulama  ID'sini giriniz", 4) or utils.getAppId()

    # dosya sistemine eristigimizde /sdcard/cenevar dizinini yoksa olustururuz (resimler burada saklanacak)
#    onFSSuccess : (fileSystem) ->
#        fileSystem.root.getDirectory settings.STORAGE_PATH, create: true, utils.onGDSuccess, utils.onGDError

    onGDSuccess : (dir) ->
        console.log "filesystem ok"


    onErr : (err) ->
        console.log err

    onFSError : (err) ->
        console.log err

    onGDError : (err) ->
        console.log err

    getDevInfo : ->
        device = device or Dvice
        return [
            ['Name '     , device.name     ],
            ['Platform: ' , device.platform ],
            ['Version: '  , device.version  ]
            ['W', $(window).width()],
            ['H', $(window).height()],
            ['OW', screen.width],
            ['OH', screen.height],
            ['Px', screen.width * screen.height],
        ]

    devResMenu : () ->
        sel = $('#devmenu select')
        sel.append($('<option>'))
        for r in RESOLUTIONS
            sel.append($("<option value='#{r[0]}'> #{r[0]}x#{r[1]}</option>"))

        sel.change (e)=>
            width = +e.target.value
            for r in RESOLUTIONS
                if width == r[0]
                    window.resizeTo(r[0] + 6, r[1] + 27)
                    document.location.reload()



# Define the click
# coodinates in x,y

# Define the buttons
# Assuming buttons do not overlap
# bottom-left point (assuming x is horizontal and y is vertical)
# upper-right point

# Which button to trigger for a click
    nearest_point : (click, buttons, max_distance=100) ->

      # Check if click is inside any of the buttons
#      for i of buttons
#        button = buttons[i]
#        bl = button[0]
#        tr = button[1]
#        return i  if (click[0] >= bl[0] and click[0] <= tr[0]) and (click[1] >= bl[1] and click[1] <= tr[1])

      # Now calculate distances
      distances = Array()
      for i of buttons
        button = buttons[i]
#        bl = button[0]
#
#        tr = button[1]
#        bl = [bl[0]-10,bl[1]-10]
#        tr = [tr[0]+10,tr[1]+10]
#        if click[0] >= bl[0] and click[0] <= tr[0]
#          distances[i] = Math.min(Math.abs(click[1] - bl[1]), Math.abs(click[1] - tr[1]))
#        else if click[1] >= bl[1] and click[1] <= tr[1]
#          distances[i] = Math.min(Math.abs(click[0] - bl[0]), Math.abs(click[0] - tr[0]))
#        else
        distances[i] = Math.sqrt((Math.pow(Math.abs(click[0] - button[0]),  2)) + (Math.pow(Math.abs(click[1] - button[1]), 2)))
      min_id = 0
      console.log "DISTANCES", distances
      for j of distances
        min_id = j  if distances[j] < distances[min_id]
      return if distances[min_id] < max_distance then min_id  else -1

#        click = Array(-1, -2)
#        button0 = Array(Array(0, 0), Array(6, 6))
#        button1 = Array(Array(10, 11), Array(17, 15))
#        button2 = Array(Array(-8, -5), Array(-3, -1))
#        i = which(click, Array(button0, button1, button2))
#        alert i

    open_external_url:(url)->
        if Dvice.isandroid
            navigator.app.loadUrl(url, { openExternal:true })
        else
            window.open(url, '_system')

    log: (tag, obj)->
        console.log("#{tag} ::: #{JSON.stringify(obj)}")

    gotid:(elm)->
        return parseInt elm.getAttribute('data-oid')


#    binder:(query, callback)->
#        $(query).click ()-> callback(utils.gotid(utils.), utils.)

    bind:(query, callback, that)->
        self = that or this
        $(query).click ()-> callback.call(self, utils.gotid(@), @)


    gevt:(evt)->
        #get object id
        return $(evt.target).find('#'+domid).data('oid')


    clicker:(callback, qry='a.LB')->
        $("div.ui-page-active #{qry}").click callback

    konsole :
        log: (m)->
            console.log "#{m.name} #{m.message}"
            #        info = {}
            #        for i in utils.getDevInfo()
            #            info[i[0]] = i[1]
            msg =
                ErrorMsg: m.message
                ErrorName: m.name
                DeviceInfo: utils.getDevInfo()


            $.post settings.SERVER_URL + 'save_client_error/', msg: JSON.stringify(msg)


#
#setTimeout (()->
#    if not document.booted
#        console.log 'tarayicidayiz'
#        document.boooted = true
#        udb.checkLocalDatabase()), 1000

#getClosestResolution = (w_h=0, width_limiter) ->
#
#    x = if w_h then $(window).height()  else $(window).width()
#    for a in RESOLUTIONS
#        if width_limiter and a[0] isnt width_limiter
#            continue
#        w = a[w_h]
#        if w <= x and (not lo or lo < w) then lo = w
#        if w >= x and (not hi or hi > w) then hi = w
#
#    lo_offset = Math.abs(x - (lo or 0))
#    hi_offset = Math.abs(x - (hi or 0))
##    console.log lo_offset, hi_offset
#    result = if lo_offset > hi_offset then hi else lo
#    return [result, result == x]
#


    #loadLayoutCss = () ->
    #    [wi, exact_wi] = getClosestResolution()
    #    [he, exact_he] = getClosestResolution(1)
    #    if (exact_wi and not exact_he) or [wi,he] not in RESOLUTIONS
    #            [ he, exact_he ] =getClosestResolution(1, wi)
    #    selected_css =  "d_#{wi}_#{he}.css"
    #    console.log "selected css #{selected_css}"
    #    $("<link rel='stylesheet' type='text/css' href='css/#{selected_css}'>").appendTo 'head'
    #    console.log getClosestResolution()
    #
    #devWeinreMenu = () ->
    #    sel = $('#devmenu select')
    #    sel.append($('<option>'))
    #    for r in RESOLUTIONS
    #        sel.append($("<option> #{r[0]}</option>"))
    #
    #    sel.change (e)=>
    #        width = +e.target.value
    #        for r in RESOLUTIONS
    #            if width == r[0]
    #                window.resizeTo(r[0]+6,r[1])
    #                window.location.reload()
    #    $("<link rel='stylesheet' type='text/css' href='css/d#{getClosestResolution()}.css'>").appendTo 'head'

