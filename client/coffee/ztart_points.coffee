start_points=

    'Nvs':  [Nav, Nav.setpoints]
    'Nvl':  [Nav, Nav.list_maps]

    'Exl':  [Evnt, Evnt.exhibitors]
    'Evl':  [Evnt, Evnt.event_list]
    'Evs':  [Evnt, Evnt.speakers]
    'Evf':  [Evnt, Evnt.favorite_list]
    'Dgl':  [Evnt, Evnt.dlg_list]
    'Spl':  [Evnt, Evnt.spn_list]
    'Pkw':  [Park, Park.show_wheels]

    'Pgl':  [Page, Page.list]

    'Cms':  [Cms, Cms.detail]

    'Phg':  [Pht, Pht.gallery]

    'Nwl':  [Nws, Nws.list]

    'Mnu':  [Mnu, Mnu.list]

    'Fbs':  [Fbck, Fbck.simple]
    'Fba':  [Fbck, Fbck.simple]



for key, val of start_points
    val[0].render = (data=null, callback)->
        display.renderPage(data, callback, @)

    val[0].bind = (query, callback)->
        utils.bind(query, callback, @)
