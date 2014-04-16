Page=
    render : (data=null, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)
    list: ()->
        if udb.cache["pages"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            @render 'template':'Page_list', 'data': {'pages': udb.cache["pages"]}, ()=>
                @bind cB, @detail


    detail:(id)->
        @render template: 'Page_detail', 'data': udb.cache["pages"][id]
