Park=
    render : (data, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)

    wheels : [
        'Harf': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'R': 'R'}
        'Rakam1': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
        'Rakam2': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
    ]

    show_wheels: (parking_lot) ->
        if parking_lot
            @save_lot parking_lot, true
        context= 'parkinglot': udb.getit('parkinglot'), 'template': 'Park_show_wheels'
        @render context, ()=>
            @set_wheels()
            @bind iB0, @set_manualy
            @bind iB1, @show_my_car


    show_my_car: ->
        if not udb.cache["parkinglot"]
            return display.showMessage "Park yeri seçilmemiş"
        for key, value of udb.cache["coordinates"]
            console.log value.name
            if udb.cache["parkinglot"] == value.name
                console.log "BULDUK"
                udb.setit 'nav_to', value.id
                udb.setit 'nav_from', value.id
                break
        if udb.getit 'nav_to'
            Nav.show_location()
        else
            Nav.navigation()


    set_wheels: ->
        $('#choose_parking_lot').scroller
            'theme': 'default'
            'display': 'inline'
            'mode': 'scroller'
            'showLabel': false
            'wheels': @wheels
            'width': document.wi * 0.19
            'height': document.he * 0.071
            'readonly': true
            'onChange': (value_text, inst) =>
                display.complete_button_action ()=> @save_lot(value_text)
        whl = $('#choose_parking_lot')
        parking_lot = udb.cache['parkinglot']
        if not parking_lot
            whl.scroller 'option', 'readonly', false
            $('.where_is_my_car_container').css(opacity: 1)
        else
            lot_arr = parking_lot.split ''
            whl.scroller 'setValue', [lot_arr[0], lot_arr[1], lot_arr[2]]

#            $('a#parking_lot_manual').live 'click', () ->
#                $('#choose_parking_lot').scroller 'option', 'readonly', false
#                $('.where_is_my_car_container').css(opacity: 1)
#                if parking_lot
#                    $('#choose_parking_lot').scroller 'setValue', [lot_arr[0], lot_arr[1], lot_arr[2]]


    set_manualy:->
        $('#choose_parking_lot').scroller 'option', 'readonly', false
        $('.where_is_my_car_container').css(opacity: 1)


    save_lot: (parking_lot, reload=false)->
        lot = parking_lot.replace /\s/g, ''
        if lot.length == 3
            udb.setit 'parkinglot', lot
#                $("#meetatpark").data('href', "meetatpark?id=#{lot}")
            if reload
                @set_wheels()
            display.showMessageBase trans.t("Parking lot %s saved", parking_lot)
        else
            display.showMessage "Invalid parking lot"




#        meetatpark: (lot)->
#            udb.vars.place.all().filter('type', '=', 60).filter('name', '=', udb.getit('parkinglot')).one (p)->
#                udb.setit 'nav_to', p.place_id
#                display.callView 'meethere', p.place_id

    # arabam nerede sayfasinda elle girilen park numarasinin kaydedilmesi

