Mnu=
    current_item_count : 1
    order : EMPTY
    order_count : 0

    render : (data=null, callback)-> display.renderPage(data, callback, @)
    bind : (query, callback)-> utils.bind(query, callback, @)

    status_messages:0: trans.t 'Selected'
                    10: trans.t 'Ordered'
                    20: trans.t 'Preparing'
                    30: trans.t 'Ready'
                    40: trans.t 'On the road'
                    50: trans.t 'On the table'
                    90: trans.t 'Return'
                    91: trans.t 'Sold out'
                    95: trans.t 'Cancel requested'
                    96: trans.t 'Canceled'

    get_table:->
        id = udb.getit('mnu_table',0)
        return if id then udb.getit('kafe_tables')[id] else null

    set_table:(id)->
        udb.setit('mnu_table',id)

    list: ()->
#        if @order is EMPTY
#            @load_orders()
        if udb.cache["menucategories"]["none"]?
            display.showMessage 'Kayıt bulunamadı'
        else
            Mnu.render  'template':'Mnu_list', 'data': udb.cache["menucategories"], ()=>
                @bind cB, @detail
                $("div.fast_product_container").each ()->
                    row = $(this)
                    item_count = row.data('len')
                    box_total = (document.wi / 4) * item_count
                    margins = item_count * 3
                    row.width(box_total + margins)

    load_orders:->
        @order = udb.getit('mnu_order',EMPTY)
        @update_order_count()

    update_order_count:->
        @order_count = Object.keys(@order).length
        $('#show_kafe_cart span').html(Mnu.order_count)

    save_order:->
        udb.setit('mnu_order', @order)
        @update_order_count()

    detail:(id)->
        @current_item_count = 1
        @render 'template': 'Mnu_detail', 'data': udb.getfromit('menuitems',id), ()=>
            $('button#add_to_chart').click ()=>
                @add_to_order(id)
            count_input = $('input[name=count]')

            $('a#urun_sayi_artir').click ()->
                @current_item_count = parseInt(count_input.val()) + 1
                count_input.attr('value', @current_item_count)

            $('a#urun_sayi_azalt').click ()->
                count = parseInt(count_input.val())
                if count > 1
                    @current_item_count =   count - 1
                    count_input.attr('value', @current_item_count)


    remove_ordered_item:(id)->
        @order[id].status = 95
        $('div#Mnu_cart tr#tr_'+id).addClass('menuitemstatus95').fadeTo(0.6);
        display.showMessage("Cancellation is delivered to the kitchen." +
                                   "Because your order was processed earlier, " +
                                   "please confirm the result of cancellation.")
        #TODO: iptal istegini sunucuya aktar

    remove_item:(id)->
        if @order[id]?
            if @order[id].status > 0
                @remove_ordered_item id
            else
                delete @order[id]
                $('div#Mnu_cart tr#tr_'+id).hide('slow')
                display.showMessage("Product removed from your order")
            @save_order()

    add_to_order:(id)->
        console.log "Order"
        console.log @order
        item = udb.getfromit('menuitems',id)
        price = if item['cut_price'] then  item['cut_price'] else item['price']
        @order[id] = {'count':@current_item_count, 'id':id, 'status':0, 'price':price}
        msg = trans.t("%s adet %s siparişinize eklendi.", @current_item_count, item.name)
        @save_order()
        @show_order()
        display.showMessage "", true, "<center><img src='images/basketfull.png' /> <br> #{msg}</center>"

    preprocess_order:->
        basket = []
        total = 0
        for id, r of $.extend(true, {}, @order)
            r['item'] = udb.getfromit('menuitems',id)
            basket.push r
            total += parseFloat r['price']
        return [basket, total]

    show_order:->
        [basket, total] = @preprocess_order()
        context = 'selected_table': @get_table(),
        'cart':basket,
        'total':total
        @render 'template': 'Mnu_cart', 'data': context, ()=>
            @bind cB, @remove_item
            @bind cB2, @detail
            @bind iB0, @send_order
            @bind iB1, @select_table_with_qrcode
            @bind iB2, @select_table_from_list
            @bind iB3, @clear_table_selection

    select_table_with_qrcode:->
        window.plugins.barcodeScanner.scan ((result) ->
            Base.qrscanner_handler result.text, 't'),
                                           ((err) ->display.showMessage "Scan failed")


    select_table_from_list:->
        tables = for id, table of udb.getit('kafe_tables')
            table
        @render 'template': 'Mnu_table_list', 'data': tables,  ()=>
            @bind cB, @table_selected

    table_selected:(id)->
        @set_table(id)
        @show_order()
        display.showMessage("Thank you. Your table selection has been saved. You can complete or continue to your order now.")

    clear_table_selection:(id)->
        @set_table(0)
        @show_order()

    send_order:->
        total  = 0
        basket = []
        for id, r of @order
            if r.status == 0
                basket.push r
                total += parseFloat r.price
        if not basket.length
            display.showMessage("",4000, "There aren't any <b>new</b> item to order.")
        else
            data =
                'items': JSON.stringify basket
                'sum':total
                'table':@get_table().id
#                customer : JSON.stringify @get_personal_info()
#                payment_metod: udb.getit 'payment_type'
            $.post settings.SERVER_URL + 'save_order/', data, (rdata)=>
                if rdata['result']=='ok'
                    @mark_order_as_processing()
                    @say_thankyou()

    say_thankyou:->
        @render 'template':'Mnu_thankyou'

    mark_order_as_processing:->
        for id, item of @order
            if item.status == 0
                item.status = 10
        @save_order()

