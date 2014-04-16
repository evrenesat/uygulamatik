Pht=
    galleryObj : null
    gallery:()->
        display.renderPage template:'gallery', 'photos':udb.cache["photos"], (()->
            $.getScript 'js/gl.js', ()->
                @.galleryObj =  $("ul#Gallery a").photoSwipe 'enableMouseWheel': false , 'enableKeyboard': false
            document.cleanup = ()->
                console.log "GERISILLL"
                document.cleanup = null
                @.galleryObj.hide()), Pht

#                    @.galleryObj.cache = null
#                    $('#gallery').remove()

#                @.galleryObj.addEventHandler(Code.PhotoSwipe.EventTypes.onHide, ()->
#                    console.log "toolbar HIDEEEEE"
#                    geri_git())
