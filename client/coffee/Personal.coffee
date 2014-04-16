Prsn=
    render : (data=null, callback)-> display.renderPage(data, callback, Prsn)
    bind : (query, callback)-> utils.bind(query, callback, Prsn)
    set_personal: (args)->
        if args and args.save_button_label
            save_button_label= args['save_button_label']
            in_tab = 'tab' in args
        else
            save_button_label = ''
            in_tab = false
        s =
            'data': @get_info()
            'template' : 'Prsn_set_personal'
            'samepage' : in_tab
        @render s, ()->
            $(aP + "input:first").focus()
            $(aP + "input,textarea").one "keydown", ()=>
                display.complete_button_action @save_data, save_button_label

    save_data:->
        args = display.urlToObj $(aP + "input,textarea").serialize()
        console.log args
        udb.setit 'name', decodeURIComponent(args.name).replace(/\+/g, " ")
        udb.setit 'email', decodeURIComponent(args.email).replace(/\+/g, " ")
        udb.setit 'tel', decodeURIComponent(args.tel).replace(/\+/g, " ")
        udb.setit 'address', decodeURIComponent(args.address).replace(/\+/g, " ")

        $(Prsn).trigger 'personal_saved'
        display.showMessage 'Kayıt işlemi başarılı'

    is_personal_info_needed: ->
        return not (udb.getit('name') and udb.getit('address') and udb.getit('email')? and udb.getit('tel'))

    get_info:->
        return {
            'name': udb.getit 'name'
            'email': udb.getit 'email'
            'tel': udb.getit 'tel'
            'address': udb.getit 'address'}


