Fbck=
    render : (data=null, callback)-> display.renderPage(data, callback, Fbck)
    bind : (query, callback)-> utils.bind(query, callback, Fbck)

    post :
        type: 'host'

    simple:(id)->
        if id
            @post.target = {'name': udb.cache["name_short"]}
            @post.mood = id
            @form()
        else
            @render feedback: @post, template: 'Fbck_survey', ()=>
                @bind cB, @simple



    form: ()->
        if Prsn.is_personal_info_needed()
            $(Prsn).one('personal_saved', @form)
            Prsn.set_personal save_button_label: "Devam Et"
        else
            @render 'template':'feedback_form', 'feedback': @post, 'user_name': udb.getit 'name', ()=>
                $('textarea#feedback_send_message').focus()
                display.showKeyboard()
                $("textarea#feedback_send_message").one "keydown", ()=>
                    display.complete_button_action @send, trans.t 'Gönder'


    send: ()->
        @post['message'] = $('#feedback_send_message').val()
        fb = @post

        data =
            'customer' : JSON.stringify Prsn.get_info()
#                oid : fb.target["#{fb.type}_id"]
            'oid' : 0
            'content_type': fb.type
            'mood': fb.mood
            'msg': fb.message
#        console.log data
        display.showLoadingMessage("Gönderiliyor...")
        $.post settings.SERVER_URL + 'save_feedback/', data, ()=>
            @render template: 'feedback_thankyou'
            display.back_to_home()
