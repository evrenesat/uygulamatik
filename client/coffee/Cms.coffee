Cms=
#    render : (data=null, callback)->
#        display.renderPage(data, callback, @)
#
#    bind : (query, callback)->
#        utils.bind(query, callback, @)

    detail:(id)->
        data = udb.cache["cms"][id]
        @render {template: 'Cms_detail', 'data': data, force_new_page: true}, =>
            @bind cB, @detail
