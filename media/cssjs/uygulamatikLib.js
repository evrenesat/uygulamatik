/**
 * User: ozgur
 * Date: 06.03.2013
 * Time: 18:44
 * To change this template use File | Settings | File Templates.
 */


(function(a){if(typeof define==="function"&&define.amd){define(["jquery"],a)}else{a(jQuery)}}(function(e){var a=/\+/g;function d(g){return g}function b(g){return decodeURIComponent(g.replace(a," "))}function f(g){if(g.indexOf('"')===0){g=g.slice(1,-1).replace(/\\"/g,'"').replace(/\\\\/g,"\\")}try{return c.json?JSON.parse(g):g}catch(h){}}var c=e.cookie=function(p,o,u){if(o!==undefined){u=e.extend({},c.defaults,u);if(typeof u.expires==="number"){var q=u.expires,s=u.expires=new Date();s.setDate(s.getDate()+q)}o=c.json?JSON.stringify(o):String(o);return(document.cookie=[c.raw?p:encodeURIComponent(p),"=",c.raw?o:encodeURIComponent(o),u.expires?"; expires="+u.expires.toUTCString():"",u.path?"; path="+u.path:"",u.domain?"; domain="+u.domain:"",u.secure?"; secure":""].join(""))}var g=c.raw?d:b;var r=document.cookie.split("; ");var v=p?undefined:{};for(var n=0,k=r.length;n<k;n++){var m=r[n].split("=");var h=g(m.shift());var j=g(m.join("="));if(p&&p===h){v=f(j);break}if(!p){v[h]=f(j)}}return v};c.defaults={};e.removeCookie=function(h,g){if(e.cookie(h)!==undefined){e.cookie(h,"",e.extend(g,{expires:-1}));return true}return false}}));

var simulator;
//noinspection JSUnusedAssignment
simulator = {
    this_is_first_load : true,
    refreshSimulator: function () {
        /**
         * refreshes simulator iframe source
         * @type {*|jQuery|HTMLElement}
         */
        var sf = $('#sim_frame');
        sf.attr("src", sf.attr("src"));
    },
    closeSimulator: function () {
        $.cookie("simulator_state", 'close');
        /**
         * destroys simulator
         */
        $('div#sim_wrapper').remove();
        this._resizeOnClose();
    },
    openSimulator: function (thiz) {
        $.cookie("simulator_state", 'open');

        /**
         * creates simulator
         * @param thiz: 'this' from calling function(one scop higher 'this')
         */
        var id = window.APPID;
        var subdomain = window.SUBD;
        if (!id) {
//            console.log('Simulatorde calisabilmek icin bir uygulama secmeniz lazim');
            return
        }
        else {

            if (location.hostname.indexOf('uygulamatik')>-1){
                var sim_url = "http://" + subdomain + ".uygulamatik.com/?aid=" + id;
            }else{
                var sim_url = "/app/index.html?aid=" + id;
            }

            var sim_wrapper = $(
                '<div id="sim_wrapper" class="sim_wrapper">' +
                    '<div id="sim_head" class="sim_head">' +
                    '<button id="sim_r_btn" class="sim_r_btn"></button><button id="sim_c_btn" class="sim_c_btn" style="float:right;"></button>' +
                    '</div>' +
                    '<iframe id="sim_frame" class="sim_frame"></iframe>' +
                    '</div>'
            );
            //simulatordeki anasayfaya donen back tusunun anapencerenin onceki sayfaya gitmesini onlemek icin
            //iframe govdesine sandbox="allow-forms allow-same-origin allow-scripts" koymayi denedim.
            //ise yaramasi gerekirdi ama yaramadi :(
            $('iframe#mainframe').before(sim_wrapper);
            this._resizeOnOpen();
            console.log(sim_url);
            $('#sim_frame').attr('src', sim_url);
            $('#sim_c_btn').bind('click', function () {
                simulator.closeSimulator();
            });
            $('#sim_r_btn').bind('click', function () {
                simulator.refreshSimulator();
            });

        }
        window.sim_frame = $('#sim_frame')[0]
        //Yalcin old
//        var sim_wrapper = $('<div></div>').attr({
//            'id': 'sim_wrapper'
//        });
//        var sim_iframe = $('<iframe></iframe>').attr({
//            'id': 'sim_frame',
//            'src': '/app/index.html?aid=' + id
//        });
//        var sim_r_button = $('<button></button>').attr({
//            'id': 'sim_r_button'
//        });
//        sim_wrapper.append(sim_r_button);
//        sim_wrapper.append(sim_iframe);
        if(simulator.this_is_first_load){
            simulator.this_is_first_load = false;
            $(window.sim_frame).live('load',function(){
                window.sim_frame.contentDocument.reset_db = true;
            });
        }
    },
    _resizeOnOpen: function () {

        var width = $('#mainframe').width();
        //var offset = $('#mainframe').offset();
        //var left = offset.left;
        $('#mainframe').width(width - 370);
        $('#mainframe').css({'right': '370px'});

    },
    _resizeOnClose: function () {
        var width = $('#mainframe').width();
        $('#mainframe').width(width + 370);
        $('#mainframe').css({'right': '0'});
    }
};
