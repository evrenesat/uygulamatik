$(document).bind("mobileinit", function(){
$.mobile.page.prototype.options.theme = document.theme;
$.mobile.page.prototype.options.headerTheme = document.theme;
$.mobile.page.prototype.options.contentTheme    = document.theme;
$.mobile.page.prototype.options.footerTheme = document.theme;
$.mobile.listview.prototype.options.headerTheme = document.theme;
$.mobile.listview.prototype.options.theme           = document.theme;
$.mobile.listview.prototype.options.splitTheme   = document.theme;
$.mobile.listview.prototype.options.countTheme   = document.theme;
$.mobile.listview.prototype.options.filterTheme = document.theme;
$.mobile.page.prototype.options.addBackBtn= false;
$.mobile.defaultPageTransition = 'none';
});
document.theme = 'a';
document.reset_db = false;
function loadLocalScript(url, success, fail){
    jQuery.ajax({
              crossDomain: true,
              dataType: "script",
              url: url+ (url.indexOf('?')>-1 ? '&':'?') + '_built=' + settings.BUILDTIME,

              timeout:1000,
              success: success,
              error: fail,
              cache: true
          })
}


//function loadJQMobile(script, textStatus){
//    loadLocalScript("js/jquery.mobile.min.js",loadUygulamatik)
//    loadUygulamatik()
//}
function loadUygulamatik(script, textStatus){
    loadLocalScript("js/uygulamatik.js", function(){$(window).trigger('uygulamatik_ready');})
}
window.appRootDirName = "uygulamatik";
function onDeviceReady(){

    window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, gotFS, fail);
    document.addEventListener("menubutton", doMenu, false);
    }

    fail = function() {
      return console.log("failed to get filesystem");
    };

    doMenu = function(){
        if(confirm("Uygulama sıfırlansın mı?")){
            persistence.reset(null, function(){setTimeout("document.location = 'index.html';",500)});

        }
    }
    gotFS = function(fileSystem) {
      console.log("filesystem got");
      return fileSystem.root.getDirectory(window.appRootDirName, {
        create: true,
        exclusive: false
      }, dirReady, fail);
    };

    dirReady = function(entry) {
      settings.STORAGE_PATH = entry.fullPath.replace('file://','');
      $(window).trigger('storageOk');
      console.log('BIOS STORAGE_PATH: ' + settings.STORAGE_PATH)
//      console.log(JSON.stringify(entry))
//      loadDefaults()
        loadUygulamatik()
      return console.log(settings.STORAGE_PATH);
    };



//function loadDefaults(){
//
//    console.log(settings.STORAGE_PATH + '/default.js')
//    loadLocalScript(settings.STORAGE_PATH + '/default.js',loadJQMobile, function(){
//        loadLocalScript('default.js?aid='+settings.APPID,loadJQMobile);
//    });
//}

function appid_from_domain() {
    dom = document.location.hostname.split('.')[0]
    var appid = 0;
    $.ajax({
        async: "false",
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        url: settings.SERVER_URL + '/appid_from_domain/' + dom,
        success: function(jsonData) {
            appid = jsonData['id']
        }
    });
    return appid
}

var sqlsupport = !!window.openDatabase;
//var sqlsupport = false;
//if (!sqlsupport){
//    persistence.store.memory.config(persistence);
//}
//$.ready(function(){
    if (!!~document.location.protocol.indexOf('http')) {
        window.downloadOnDemand = function(){}
        console.log('ORTAM : #### WEB ####')
        document.on_the_web = true
        settings.STORAGE_PATH =  settings.STATIC_SERVER_URL + "media/uploads/";
        if(window['APPID']){
            settings.APPID = APPID;
        }else if(document.location.search.indexOf('aid')>-1){
            aid = parseInt(document.location.search.replace('?aid=',''));
            if(aid && !isNaN(aid)){
                settings.APPID = aid;
            }
        }else{
            settings.APPID = appid_from_domain()
        }
//        loadDefaults();
//        loadJQMobile();
        loadUygulamatik();
    }else{
        document.addEventListener("deviceready", onDeviceReady, false);
    }
//});
