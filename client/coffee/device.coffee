Dvice =
    name: null
    platform: null
    version: null
    vdigit: 0 #first digit of os version
    isandroid: null
    isios: null
    pixels: screen.width * screen.height
    power: 3 #1: low, 2: mid, 3:hi end, 4: super hi end  device
    # cpu & gpu power, generally related with total pixels (screen resolution)
    caps: 2 #0: incapable, 1, capable, 2: superior
    #caps is for webkit capabilities eg. overflow:scroll, position:static support
    #old iphones and 2x androids are incapable ones
    less_parser: less.Parser()
    less_css: []
#    less_predefined: utils.getDocSize()
    init: ->
        if window.device?
            Dvice.name = device.name
            Dvice.platform = device.platform
            Dvice.version = device.version
            Dvice.deviceDedector()
        else
            Dvice.uaDedector()
        if Dvice.version
            Dvice.vdigit = parseInt(Dvice.version.substring(0, 1))
        if Dvice.platform
            Dvice.processDeviceInfo()
        Dvice.customizeSettings()
        Dvice.applyCSSPatches()


    processDeviceInfo: ->
        if Dvice.isandroid then Dvice.processAndroid()
        else if Dvice.isios then Dvice.processios()


    deviceDedector: ->
        Dvice.dedectAndroid() or Dvice.dedectiOS()


    dedectAndroid: ->
        if Dvice.platform == 'Android'
            Dvice.isandroid = true

            return true

    processAndroid: ->
        #pixel miktari cihazin cpu/ram gucu hakkinda ipucu veriyor.
        if Dvice.pixels > 400000
            Dvice.power = 4
        else if Dvice.pixels < 400000
            Dvice.power = 3
        else if Dvice.pixels < 150000
            Dvice.power = 2
        else if Dvice.pixels < 100000
            Dvice.power = 1
        if Dvice.vdigit < 4
            Dvice.caps = 0
        console.log "power: #{Dvice.power}"
        console.log "caps: #{Dvice.caps}"


    processios: ->
        #notging to do for now


    dedectiOS: ->
        osnames = ['iPhone', 'iPad', 'iPhone Simulator', 'iPad Simulator']
        if osnames.indexOf(Dvice.device.platform) > -1
            Dvice.isios = true


    uaDedector: ->

        if Dvice.uaAndroidDedector()
            return
        if Dvice.uaiosDedector()
            return
        Dvice.version = '4.0.0'


    uaAndroidDedector: ->
        ua = navigator.userAgent
        #FIXME regexle gercek surum noyu okumak yerine majorla yetiniyoruz
        #        console.log "andro 2mis: ", ua.indexOf 'Android 2'
        #        console.log "andro 2mis: ", typeof(ua.indexOf 'Android 2')
        if ua.indexOf('Android 2') > -1
            Dvice.platform = 'Android'
            Dvice.version = '2.0.0'
        else if ua.indexOf('Android 4') > -1
            Dvice.platform = 'Android'
            Dvice.version = '4.0.0'
        if Dvice.version
            Dvice.isandroid = true
            return true



    uaiosDedector: ->
        ua = navigator.userAgent
        #FIXME regexle gercek surum noyu okumak yerine majorla yetiniyoruz
        if (ua.indexOf('iPhone OS 5') + ua.indexOf('iPad OS 5') + ua.indexOf('iPod OS 5')) > -1
            Dvice.platform = 'iPhone'
            Dvice.version = '5.0.0'
        else if (ua.indexOf('iPhone OS 4') + ua.indexOf('iPad OS 4') + ua.indexOf('iPod OS 4')) > -1
            Dvice.platform = 'iPhone'
            Dvice.version = '4.0.0'
        if Dvice.version
            Dvice.isios = true
            return true


    customizeSettings: ->
        if Dvice.isandroid
            Dvice.androidCustomizations()
        else if Dvice.isios
            Dvice.iosCustomizations()
        Dvice.generalCustomizations()

    generalCustomizations: ->
        console.log "general custom "
        #TODO: saydam listeler icin baska bir belirtec bulacagiz
#        if Dvice.caps > 1
#            if document.theme =='b'
#                Dvice.less_css.push """
#                               ul.ui-listview li:active {
#                                 background-color: #000;
#                               }
#                               ul.ui-listview li {
#                                 background: none;
#                                 background-image: none;
#                                 background-color: rgba(0, 0, 0, 0.50);
#                               }
#                               """

    androidCustomizations: ->
        console.log "DEV android customizations"
        Dvice.less_css.push """
                        div.ui-page-active > ul{-webkit-transform: translate3d(0, 0, 0);}
                       .tridi{-webkit-transform: translate3d(0, 0, 0);}
                       .dev_fast_placebox{-webkit-transform: translate3d(0, 0, 0);}
                       """
        document.default_transition = 'none'
        settings.record_per_page = Dvice.power * 15
        Paginator.max_records = Dvice.power * 70
#        console.log "perpage #{Um.record_per_page}"
#        if Dvice.caps < 1 and document.theme =='a'
#            Dvice.less_css.push """
#                           #products, #places, #campaigns {
#                           background-color:rgb(87,87,87);
#                           }
#                           ul.ui-listview li {
#                           background: none;
#                           background-image: none;
#                           background-color: rgb(0, 0, 0);
#                           }
#                           """




    iosCustomizations: ->
        console.log "ios css patch"
        document.default_transition = 'fade'
        Dvice.less_css.push """
                       .tridi{-webkit-overflow-scrolling: touch;}
                       .dev_fast_placebox{-webkit-overflow-scrolling: touch;}
                       """


    applyCSSPatches: ->
        console.log "APPLY css patches"
        if Dvice.less_css.length
            Dvice.renderLess(Dvice.less_css.join("\n"), utils.getDocSize())


    renderLess: (lesstring, prefix) ->
        console.log "APPLY PATCH PRE >> #{prefix}"
        console.log "APPLY PATCH >> #{lesstring}"
        Dvice.less_parser.parse prefix + lesstring, (e, tree)=>
            console.log "HEAD HEAD HEAD"
            console.log tree
            $('head').append("<style id='patch' type='text/css'>#{tree.toCSS()}</style>")

