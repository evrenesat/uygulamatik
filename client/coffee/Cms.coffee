Cms=
#    render : (data=null, callback)->
#        display.renderPage(data, callback, @)
#
#    bind : (query, callback)->
#        utils.bind(query, callback, @)

    detail:(id)->
        console.log "CMS DETAILL"
        data = udb.cache["cms"][id]
#        data['title'] = data.title
        @render {template: 'Cms_detail', 'data': data, force_new_page: true}
        @bind cB, @detail
