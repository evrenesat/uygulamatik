(function($) {
    base_url = 'http://chart.googleapis.com/chart?chf=a,s,000000&chs=200x200&cht=qr&chld=|2&chl=http%3A%2F%2Ff0b.in%2F'
    if ($('#id_type') && $('#id_type').val()=="60"){
        url = base_url + "a" + $('#id_name').val()
    }else{
        p=document.location.pathname.split('/')
        id = p[p.length-2]
        type = p[p.length-3]
        url = base_url + "s" + $('#id_name').val()
    }
})(django.jQuery);
