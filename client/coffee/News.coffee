Nws=
    render : (data=null, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)
    list: ()->
        if udb.cache["news"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            @render template:'Nws_list', 'data': {'news': udb.cache["news"]}, ()=>
                @bind cB, @detail


    detail:(id)->
        @render template: 'Nws_detail', 'data': udb.cache["news"][id]
