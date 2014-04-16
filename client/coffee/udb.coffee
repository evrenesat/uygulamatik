udb =
    vars:
        'DB_SIZE': 5 * 1024 * 1024
        'img_dir': '/sdcard/cenevar'
        'place': null
        'product_category': null
        'store_product_category': null
        'product': null
        'campaign': null
        #        version: null
        'chart': null
        #        settings: null
        'dbsettings': null
        'activity': null
        'in_mem_data':
            {}
        'db_schema_version': 37
    force_reload: false
    cache: {}
#    settings_save_stack: []
#    settings_save_in_process : false
    prefixed_settings:
        'favevents':[]
        'favexhibitors':[]
#        'modules':[]
        'favexhibitorfiles':[]
#        'appid':''

    background_saver:->
        ### kaydedilecek verileri sirayla kaydeder.  ###
#        console.log "SETiT STACK SIZE #{document.save_settings_stack.length}"
        keyval = document.save_settings_stack.shift()
        if keyval
            try
#                console.log "SETiT KEYVAL #{JSON.stringify(keyval[0])}"
                key = keyval[0]
                val = keyval[1]
#                console.log "SETiT for #{key} => #{val}"
                udb.vars['dbsettings'].all().filter('key', '=', key).one (s) =>
        #            val = udb.cache[key]
        #            console.log "SETiT #{key} #{val} >> entity type  #{typeof(s)} #{JSON.stringify(s)}"
                    if s is null
#                        console.log "SETiT #{key} YOK  YARATILACAK"
                        s = new udb.vars['dbsettings'] 'key': key, 'val': JSON.stringify val
                        persistence.add(s)
                    else
#                        console.log "SETiT MEVCUT GUNCELLENECEK  #{key}"
#                        console.log val
                        s.val = JSON.stringify val
                    persistence.flush(udb.background_saver)
            catch e
                document.settings_save_in_process = false
                console.log e
        else
#            console.log "SETiT STACK EMPTY"
            document.settings_save_in_process = false

    start_background_saver:->
        if not document.settings_save_in_process
#            console.log "SAVE PROCESS STARTED"
            document.settings_save_in_process = true
            udb.background_saver()
        else
#            console.log "SAVE ALREADY RUNNING"

    setit: (key, val) ->
        ###asil kayit islemi background_saver tarafindan arkaplanda yapilacak###
#        console.log "SETiT just Setit #{key}"
        udb.cache[key] = val
        document.save_settings_stack.push [key, val]

#    setit: (key, val) ->
#        console.log "SETiT #{key}"
#        udb.cache[key] = val
#        udb.vars['dbsettings'].all().filter('key', '=', key).one (s) =>
#            if s is null
#                console.log "SETiT #{key} YOK  YARATILACAK"
#                s = new udb.vars['dbsettings'] 'key': key, 'val': JSON.stringify val
#                persistence.add(s)
#            else
#                console.log "SETiT MEVCUT GUNCELLENECEK  #{key}"
#                s.val = JSON.stringify val
#            persistence.flush()
#



    #            console.log "key: #{key}, val: #{JSON.stringify(val)}"
    getfromit:(key,id)->
        #FIXME: burada sozluk copyaliyoruz, aksi halde nesne sayfanin render islemi sirasinda bozuluyor
        #sorun udb.cache['menuitems'] udb.background_saver icinde json.stringfy ile serialize edilirken
        # circular reference error gibi bir hatayla kendini gostriyor
        return $.extend({}, udb.cache[key][id])

    getit: (key, dflt) ->
#        console.log "getit #{key} #{udb.cache[key]}"
        return if udb.cache[key]? then udb.cache[key] else dflt or ''



    #    delsql:(tx)->
    #        tx.executeSql "select 'drop table ' || name || ';' from sqlite_master where type = 'table';"
    #        tx.executeSql "CREATE TABLE `activities` (`activity_id` INT, `name` TEXT, `description` TEXT, `start_date` DATETIME, `end_date` DATETIME, `image` TEXT, `id` VARCHAR(32) PRIMARY KEY)", [],
    #        (tx,results)=> console.log('ok',results),
    #        (tx,err)=> console.log( err)
    #
    #    deleteAllTabels:(callback)->
    #        udb.rdb = openDatabase(settings.DB_NAME, '1.0', settings.DB_NAME, udb.vars['DB_SIZE'])
    #        udb.rdb.transaction udb.delsql,
    #        (tx,res)=> console.log(res),
    #        (tx,err)=> console.log(err)


    deleteAllTables: (callback)->
        console.log "OPENDB", sqlsupport
#        udb.rdb = openDatabase(settings.DB_NAME, '1.0', settings.DB_NAME, udb.vars['DB_SIZE'])
        udb.rdb.transaction (tx)=>tx.executeSql 'select tbl_name from sqlite_master where type = ?;', ['table'],
        (tx, results)=>
            console.log 'tables length', results.rows.length
            for i in [0...(results.rows.length)]
                tbl_name = results.rows.item(i).tbl_name
                if tbl_name.indexOf('__') == -1
                    tx.executeSql "drop table '#{tbl_name}';"
            #                            tx.executeSql "drop table '#{tbl_name}';",(()=>),((tx,err)=>console.log err)

            setTimeout (()=>callback && callback()), 300
        ,
        (tx, err)=>
            console.log "error"

    initDB: (callback)->

        udb.rdb = openDatabase(settings.DB_NAME, '1.0', settings.DB_NAME, udb.vars['DB_SIZE'])
        udb.rdb.transaction (tx)=>tx.executeSql 'select * from activities;', [], callback, (()=>udb.insertSQL(callback))


    #    initImages:()-> #COP COP COP?????
    #        images_dir = '.forumbornova'
    #        window.requestFileSystem LocalFileSystem.PERSISTENT, 0, ((fileSystem) =>
    #            fileSystem.root.getDirectory "file:///android_asset/www/images", create: false, (entry) =>
    #                console.log "get existing files"
    #                reader = entry.createReader()
    #                reader.readEntries ((files) => udb.fetchFiltered files), utils.onErr
    #        ), utils.onErr


    #        parentEntry = new DirectoryEntry({fullPath:images_dir})



    insertSQL: (callback)->
        $.get "initial.sql", (sqltext)=>
            console.log "InsertSQL"
            lines = $.trim(sqltext.replace(/\n/g, '')).split(');')
            #            console.log lines
            udb.rdb.transaction (tx)=>
                for l in  lines
                    if l then tx.executeSql l + ')'
                #                        if l
                #                            l = l+ ')'
                #                            tx.executeSql(l, [], ((tx,res)->)
                #                            ,((tx,err)->console.log("a#{l}a",tx,err))
                #                            )
            ,
            (tx, err)=>
                console.log("err InsertSQL")
#                delete udb.rdb
            ,
            ()=>
                callback()
                console.log("ok InsertSQL")
        callback()
#                delete udb.rdb



    checkLocalDatabase: ->
        if sqlsupport
            udb.initDB ()=>udb.initPersistence()
        else
            udb.initPersistence()


    initPersistence: ->
        console.log "DB CHECK"
        #        persistence.debug = true
        # istenilen isimde db yoksa yaratir
#        console.log(udb.)
        if sqlsupport
            persistence.store.websql.config persistence, settings.DB_NAME, settings.DB_NAME, udb.vars['DB_SIZE']
        else
            persistence.store.memory.config(persistence)
        #        persistence.reset()
        udb.defineDataModel ()=>
            #            console.log "defdatamodel cb"
            udb.fill_cache ()=>
                #                console.log "fill_Settings cb"
                udb.evolveDBSchema ()=>
                    if (navigator.connection? and navigator.connection.type isnt Connection.NONE) or document.on_the_web
                        udb.versionComparison()
#                        udb.getMapGraph()
                    else
                        console.log 'BAGLANTI YOK'
                        display.showLoadingMessage('Ağ bağlantısı yok. Güncelleme kontrolü yapılamadı', 5000)


    #        display.callView('fastfooders')

    fill_try_no: 0
    fill_cache: (fn) ->
        console.log "READSET START ##{udb.fill_try_no}"
        a=''
        udb.vars['dbsettings'].all().list (dbsettings) =>
#            console.log "READSET #{JSON.stringify(dbsettings)}"
            $.each dbsettings, (index, seting)=>
                if seting.val and '[{'.indexOf(seting.val.charAt(0)) >= -1
                    udb.cache[seting.key] = JSON.parse seting.val
                else
                    udb.cache[seting.key] = seting.val
                a+=seting.key
#                console.log "READSET #{seting.key}"
#                if seting and seting.key == 'modules'
#                    alert('AAAA')

            if not udb.cache['appid']
                udb.force_reload = true
                console.log "APPID NOT CACHED"
            else if not udb.cache['modules']
                console.log "MODULES NOT CACHED #{JSON.stringify(udb.cache['modules'])}"
                udb.fill_try_no +=1
                if udb.fill_try_no <= 3
                    udb.force_reload = true
                else
                    console.log "Giving Up! After 3 failures, modules data still unavailable"
            if settings.APPID
                udb.setit('appid', settings.APPID)
            if not udb.getit('appid')
                appid = utils.getAppId()
                udb.setit('appid', appid)
                console.log "READSET NEW APPID #{udb.getit('appid')}"
            if settings.SERVER_URL.indexOf('api1/') == -1
                settings.SERVER_URL  = settings.SERVER_URL + 'api1/' + udb.getit('appid', 0) + "/"
            udb.setit('static', settings.STORAGE_PATH)

            for k in Object.keys(udb.prefixed_settings)
                if not udb.getit(k)
                    udb.setit k, udb.prefixed_settings[k]
            fn()
#            window.tv = udb.cache
            if udb.cache['modules']? and udb.cache['modules'].length
                udb.module_names = (m['codename'] for m in udb.cache['modules'])
            $(window).trigger('settingsOK')
            $(document).trigger('cache_filled')

    #db sema surumu degistiyse dbyi verilerle birlikte silip yeniden olusturuyoruz.
    evolveDBSchema: (callback)->
        current_version = udb.getit 'schema_version'
        #        console.log JSON.stringify Um.cache
        #        console.log udb.getit 'schema_version'
        if current_version != udb.vars['db_schema_version']
            display.showLoadingMessage(trans.t('Please wait, updating application data.'))
            try
                console.log "db surumu farki: #{udb.vars['db_schema_version']} != #{current_version}"
                persistence.reset () =>
                    console.log "resetlendi"
                    persistence.schemaSync () =>
                        udb.getRecords()
                        udb.setit 'schema_version', udb.vars['db_schema_version']
                        callback()
            catch e
            #                $.mobile.loading 'hide'
                console.log e.message


        else
            callback()



    # kullanilacak ve tablosu olusturulacak veri modellerinin tanimlanmasi
    defineDataModel: (callback) ->
        udb.vars['place'] = persistence.define 'places',
            'place_id': "INT",
            'category_id': "INT",
            'type': "INT",
            'node__map_id': "INT",
            'node': "INT",
            'name': "TEXT",
            'description': "TEXT",
            'authorized_person': "TEXT",
            'address': "TEXT",
            'phone': "TEXT",
            'template': "TEXT",
            'gsm': "TEXT",
            'email': "TEXT",
            'logo': "TEXT",
            'background': "TEXT"
            'favorite': "BOOL",
        udb.vars['place'].index 'place_id', unique: true
        udb.vars['place'].index 'name'
        udb.vars['place'].index 'type'
        # performans icin indexleme islemi

        udb.vars['product_category'] = persistence.define 'product_category',
            'product_category_id': "INT",
            'image': 'TEXT'
            'name': "TEXT"
        udb.vars['product_category'].index 'product_category_id', unique: true

        udb.vars['store_product_category'] = persistence.define 'store_product_category',
            'place_id': "INT",
            'order': "INT",
            'store_product_category_id': "INT",
            'name': "TEXT"
        udb.vars['store_product_category'].index 'store_product_category_id', unique: true

        udb.vars['product'] = persistence.define('products',
            {'product_id': "INT",
            'category_id': "INT",
            'store_category_id': "INT",
            'place_id': "INT",
            'name': "TEXT",
            'description': "TEXT",
            'showcase': "BOOL",
            'price': "INT",
            'cut_price': "INT",
            'discount_rate': "INT",
            'image': "TEXT"})
        udb.vars['product'].index 'product_id', unique: true
        udb.vars['product'].index 'name'
        udb.vars['product'].index 'showcase'

        udb.vars['campaign'] = persistence.define 'campaigns',
            'campaign_id': "INT",
            'category_id': "INT",
            'place_id': "INT",
            'type': "INT",
            'product_id': "INT",
            'name': "TEXT",
            'description': "TEXT",
            'no_text': "BOOL",
            'start_date': "DATETIME",
            'end_date': "DATETIME",
            'stock': "INT",
            'image': "TEXT"
            'thumb_image': "TEXT"
            'special_background': "TEXT"
        udb.vars['campaign'].index 'campaign_id', unique: true


        udb.vars['activity'] = persistence.define 'activities',
            'activity_id': 'INT',
            'name': 'TEXT',
            'description': 'TEXT',
            'start_date': 'DATETIME',
            'end_date': 'DATETIME',
            'image': 'TEXT'
        udb.vars['activity'].index 'activity_id', unique: true


        udb.vars['chart'] = persistence.define 'chart',
            'product_id': 'INT',
            'count': 'INT'

        udb.vars['dbsettings'] = persistence.define 'dbsettings',
            'key': 'TEXT',
            'val': 'TEXT',


        # modeller arasi iliskilerin belirtilmesi
        udb.vars['product_category'].hasMany 'categories', udb.vars['product_category'], 'upper_category'
        udb.vars['product_category'].hasMany 'products', udb.vars['product'], 'category'
        udb.vars['product_category'].hasMany 'places', udb.vars['place'], 'category'
        udb.vars['product_category'].hasMany 'campaigns', udb.vars['campaign'], 'category'

        udb.vars['store_product_category'].hasMany 'products', udb.vars['product'], 'store_category'

        udb.vars['place'].hasMany 'store_product_category', udb.vars['store_product_category'], 'place'
        udb.vars['place'].hasMany 'products', udb.vars['product'], 'place'
        udb.vars['place'].hasMany 'campaigns', udb.vars['campaign'], 'place'
        udb.vars['product'].hasMany 'campaigns', udb.vars['campaign'], 'product'
        udb.vars['chart'].hasOne 'product', udb.vars['product']

        # modellerin veritabaniyla senkronizasyonu
        console.log "INIT SCHEMA"
        persistence.schemaSync () =>
            callback()

#
#    getMapGraph: ->
#        url = settings.SERVER_URL + 'map_graph/?a=' + Math.ceil(Math.random() * 1000)
#        $.getJSON url, (data) =>
#            udb.setit('mapgraph', data)
#        , 'json'

#    cacheCoordinates: (data) ->
#        coordinates = {}
#        $.each data.places, (index, place)=>
#            coordinates[place.place_id] = {x: place.x, y: place.y}
#        udb.setit('coordinates', coordinates)

    reset_db:->
#        udb.force_reload = true
#        $(udb).bind 'cache_filled', ()->
        persistence.reset()
        udb.cache = []
        $(window).trigger('uygulamatik_ready');

#        setTimeout((()->udb.fill_cache(views.Base.index)), 6000)
#        udb.versionComparison()

    # sunucu db ile cihaz db versiyon karsilastirma
    versionComparison: (notification = false) ->
        # phonegap'in sorgulari cache'lemesi sorununu asmak icin linkin sonuna rasgele olusturulan bir sayi eklenmekte
        url = settings.SERVER_URL + 'get_version/?xxrnd=' + udb.get_random()
#        utils.log "VCOMP url", url
        $.getJSON url, ((data) =>
#            utils.log "VCOMP VersionComp", data
            current_data_version = udb.getit 'data_version'
            new_data_version = data.current_version
            if data['current_version'] isnt current_data_version or document.reset_db
                if document.reset_db
                    document.reset_db = false
                    udb.cache = []
#                console.log "VCOMP data['current_version'] isnt current_data_version #{data['current_version']} !== #{current_data_version}"
                display.showLoadingMessage('Lütfen bekleyin. Veritabanı güncelleniyor.')
                # sadece tarayici belleginde olacagi icin settings ve chart tablosunun yedegini aliriz
                persistence.dump [udb.vars['dbsettings'], udb.vars['chart']], (data) =>
#                    console.log "VCOMP dumped"
                    persistence.reset () => # veritabanini komple sileriz
                        console.log "VCOMP deleted"
                        persistence.schemaSync () => # tablolar yeniden olusur
                            console.log "VCOMP recreated"
                            persistence.load {'dbsettings': data['dbsettings'], 'chart': data['chart']}
#                            console.log "VCOMP reloaded"

                            # settings ve chart ayarlari olusur
                            udb.getRecords()
                            # geri kalan veriler de sunucudan cekilir.
                            udb.setit 'data_version', new_data_version
#                console.log "VCOMP APPID:::: :#{udb.cache['appid']}"
                udb.setit('appid', udb.cache['appid'])

            else
                if notification
                    $.mobile.hidePageLoadingMsg()
                    display.showMessage 'Uygulama Guncel Durumda'
        ), 'json'

    get_random:->
        Math.ceil(Math.random() * 100000)

    # sunucudan kayitlari cekme
    we_get_local_records : false
    getRecords: (lang = '') ->
        try
            if lang
                if udb.we_get_local_records
                    console.log "local data already fetched, returning"
                    return
                udb.we_get_local_records = true
            console.log "GETRECORDS lang #{lang}",
            url = "#{settings.SERVER_URL}get_all_records/?lang=#{lang}&xrnd=#{udb.get_random()}"
            console.log "GETRECORDS #{url}"
            $.getJSON url, ((data) =>
                udb.addRecords data
                udb.getThemeCSS() #TODO: bu burda olmamali. tema degismedigi surece yenilenmemeli
            ), 'json'
        catch ex
            console.log ex
            udb.setit 'data_version', 0

    saveAppInfo: (data) ->
#        console.log appinfo
#        debugger
        appinfo = data['appinfo'][0]

        for key in Object.keys(appinfo['fields'])
            udb.setit key, appinfo['fields'][key]
#            udb.cache[key] = appinfo['fields'][key]
        for key in Object.keys(data['simple_data'])
            udb.setit key, data['simple_data'][key]
#            udb.cache[key] = data['simple_data'][key]
#        udb.setit('modules',data.modules)
    # sunucudan gelen bilgilerin cihaz veritabanina eklenmesi
    addRecords: (data, notification = false) ->
        console.log "c"
        persistence.load {
        'product_category': data['categories'],
        'places': data['places'],
        'store_product_category': data['store_product_categories'],
        'products': data['products'],
        'campaigns': data['campaigns'],
        },

        () =>
            console.log "ADDRECORDS PERSISTENCE LOAD OK"
            udb.saveAppInfo(data)
#            setTimeout (()=>document.location = "index.html"),1000

            udb.fill_cache ()->
                $.mobile.loading 'hide'
#                udb.setit("defaulttheme", udb.cache.jmt)
                setTimeout (()=>udb.writeDefaultJS()),500
            display.showMessage trans.t 'Güncelleme Başarılı'
            if not document.on_the_web
                setTimeout (()=>display.showLoadingMessage('Lütfen bekleyiniz, görsel ögeler indiriliyor. İnternet hızınıza bağlı olarak bu işlem birkaç dakika sürebilir. ')), 1000

            udb.fetchImages data['images']

    # eger notification varsa (orn: ayarlar sayfasindaki guncelleme secenegi) guncellemeyle ilgili uyari verir

    ##        $.mobile.loading 'hide'

    getThemeCSS: ()->
        console.log "getThemeCSS!"
        if not document.on_the_web
            $.get settings.SERVER_URL + 'get_css/', (data)->
                udb.writer('theme.css',data)
                setTimeout udb.loadThemeCSS,300

    loadThemeCSS: ()->
        if document.on_the_web
            cssurl = settings.SERVER_URL + 'get_css_for_web/?rand=' + udb.get_random()
        else
            cssurl = "#{settings.STORAGE_PATH}/theme.css"
        console.log "LOAD THEME CSS"
        console.log cssurl
        $('head').append("<link rel='stylesheet' href='#{cssurl}'/>")

    justImages: () ->
        console.log "just_images"
        if document.on_the_web
            return
        url = settings.SERVER_URL + 'get_image_list/?xrnd=' + udb.get_random()
        $.getJSON url, ((data) =>
            setTimeout (()=>display.showLoadingMessage('Lütfen bekleyiniz, görsel ögeler indiriliyor. İnternet hızınıza bağlı olarak bu işlem birkaç dakika sürebilir. ')), 500
            udb.fetchImages data.images

        ), 'json'


    fetchImages: (images) ->
        if document.on_the_web
            console.log "We are on the WEB"
            return
        # cihazin dosya sistemine erisiriz
        udb.fetch_list = images
        console.log "FTCH images... #{JSON.stringify(images)}"

        #        alert('Lütfen bekleyiniz, görsel ögeler indiriliyor.')
        window.requestFileSystem LocalFileSystem.PERSISTENT, 0, ((fileSystem) =>
            fileSystem.root.getDirectory settings.STORAGE_PATH, create: false, (entry) =>
                console.log "FTCH get existing files"
                reader = entry.createReader()
                reader.readEntries ((files) => udb.fetchFiltered files), utils.onErr
        ), utils.onErr


    syncDownloader: (thread_no)->
        tid = "DLTHD##{thread_no}"
        item = if udb.stack[thread_no]? then udb.stack[thread_no].shift() else null
        if item
            ft = new FileTransfer()
            source = "#{settings.STATIC_SERVER_URL}media/uploads/#{item}"
            target = "#{settings.STORAGE_PATH}/#{item}"
            console.log("FTCH source: #{source} target: #{target}")
            ft.download source, target, (()=>udb.syncDownloader thread_no), (()=>udb.syncDownloader thread_no)
        else
            console.log "#{tid} FINISHED"
            delete udb.stack[thread_no]
            if not Object.keys(udb.stack).length
                console.log "ALLLLLL FINISHED AT #{tid}"
                display.showMessage "Güncelleme tamamlandı"
                Base.index()

    stack:
        {}
    fetchFiltered: (files) ->
        console.log "fetch non-existing files"
        fileTransfer = new FileTransfer()
        images=[]
        filter_list = []
        filter_list.push f.name for f in files
        images.push f for f in udb.fetch_list when f not in filter_list

        #es zamanli download sayisi
        number_of_threads = Dvice.power * 1
        console.log "HOW MANY THREADS ::: #{number_of_threads}"
        #parseInt'in asagi yuvarlamasi ihtimaline karsi +1 yapiyoruz.
        queue_size = parseInt((images.length / number_of_threads) + 1)

        start = 0
        console.log "sunucuda: #{udb.fetch_list.length} yerelde: #{filter_list.length} indirilecek: #{images.length}"
        console.log "queue_size #{queue_size}"
        for i in [0..(number_of_threads - 1)]


            console.log "DL QUEUE FOR THD##{i} :::: #{start}..#{start + queue_size}"
            #aslinda baslangic haricinde 2 .. yerine 3 ... nokta kullanmamiz gerekirdi
            #ama ayni gorseli tekrar indirmeye calismaktan zarar gelmez.
            udb.stack[i] = images[start..start + queue_size]
            udb.syncDownloader i
            start = start + queue_size


    #            console.log udb.fetch_list
    #            console.log filter_list

    #        udb.downloadcount = 0
    #        udb.totalimg = images.length
    #        udb.download_ok_interval = setInterval ()=>
    #            if udb.downloadcount >= (udb.totalimg - 1)
    #                $.mobile.loading 'hide'
    #                clearInterval(udb.download_ok_interval)
    #        ,2000
    #        for i in images
    #            domain = settings.SERVER_URL + 'media/uploads/' + i
    #            #                console.log 'domain: ' + domain
    #            target = udb.vars['img_dir'] + '/' + i
    #            #                console.log 'target: ' + target
    #            fileTransfer.download domain, target, (()=>
    #                console.log "DOWNLOAD COMPLETE:: #{udb.downloadcount} == #{(udb.totalimg - 1)}"
    #                udb.downloadcount+=1
    #
    #            ),()=>
    #                udb.downloadcount+=1
    #




    #            console.log "img dwn cmplt #{udb.downloadcount} / #{udb.totalimg}"

    writeDefaultJS: ()->
#        content = "document.theme = '#{udb.getit("defaulttheme", 'a')}'"
#        udb.writer("default.js", content)

    writer: (filename, content)->
        if LocalFileSystem?
            window.requestFileSystem LocalFileSystem.PERSISTENT, 0, ((fileSystem) =>
                fileSystem.root.getFile "#{settings.STORAGE_PATH}/#{filename}", create: true, (entry) =>
                    entry.createWriter ((writer)=>writer.write(content)), utils.onErr

            ), utils.onErr

    setStoragePath: ()->
        window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, gotFS, fail)
        fail=() ->
            console.log("failed to get filesystem")

        gotFS=(fileSystem)->
            console.log("filesystem got");
            fileSystem.root.getDirectory(window.appRootDirName, {
            create: true,
            exclusive: false
            }, dirReady, fail)


        dirReady=(entry)->
            settings.STORAGE_PATH = entry + settings.STORAGE_DIRNAME
            $(window).trigger('storageOk')
            console.log(settings.STORAGE_PATH)

