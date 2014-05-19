Cms=
    render : (data=null, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)

    detail:(id)->
        @render template: 'Page_detail', 'data': udb.cache["cms"][id]
