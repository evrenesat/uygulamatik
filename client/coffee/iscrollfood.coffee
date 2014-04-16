iScrollFood=
    cache:[]
    initOk:false


    init:->
        console.log "iscroll caps #{Dvice.caps}"
        if Dvice.caps > 1
            return #dev (hopefully) supports native overflow:auto
#        console.log "manual scroll devices power #{Dvice.power}"
        iScrollFood.initOk = true
        console.log "iSCROLLFOOOD init caps #{Dvice.caps}"
        iScrollFood.cache=[]
#        document.addEventListener('touchmove', iScrollFood.preventer, false)
        document['cleanup'] = ()=>
            console.log "cleanup on #{document.page_id}"
            if not document.page_id
                iScrollFood.cleanup()

    preventer: (e)->
        e.preventDefault()

    cleanup:->
        try
            if iScrollFood.initOk
                for scroller in iScrollFood.cache
                    scroller.destroy()
                    scroller = null
                iScrollFood.initOk = false
                document.removeEventListener('touchmove', iScrollFood.preventer, false)
                console.log "FOOOOOOOODscroll temizlendi"
                document.cleanup = null
        catch error
            console.log "err: #{error}"

    scrollThis:(id,prefix='')->
        if iScrollFood.initOk
            console.log "SETTING iSCROLLFOOD #{id}"
            myScroll = new iScroll "#{prefix}fid# {id}",
                bounce:false
                hScrollbar:false
                vScrollbar:false
                vScroll: false,
                onBeforeScrollStart: iScrollFood.obss
            iScrollFood.cache.push myScroll
            setTimeout (()=>myScroll.refresh()),100
    ###*@this {myScroll}###
    obss:( e )->
        ###
        @this {iScrollFood}
        ###
        if ( this.absDistX > (this.absDistY + 5 ) )
            # user is scrolling the x axis, so prevent the browsers' native scrolling
            e.preventDefault()
