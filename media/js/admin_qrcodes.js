$(function(){
    base_url = 'http://chart.googleapis.com/chart?chf=a,s,000000&chs=200x200&cht=qr&chld=|2&chl=http%3A%2F%2Ff0b.in%2F';
    url = '';
//    base_url = 'http://chart.googleapis.com/chart?chf=a,s,000000|bg,lg,0,EFEFEF,0,BBBBBB,1&chs=200x200&cht=qr&chld=|2&chl=';

    p = document.location.pathname.split('/')
    id = p[p.length - 2]
    type = p[p.length - 3]

    if (isNaN(id)){
        return false
    }

    if (type=='store'){
        if ($('#id_type').val() == "60") {
            url = base_url + "a" + $('#id_name').val()
        } else {
            url = base_url + "s" + id
        }
    }else if (type=='ordertable'){
        url = base_url + "t" + id
    }else if (type=='product'){
            url = base_url + "p" + id
        }
    if(url)$('body').append("<img src="+url+" style='position:absolute;top:150px;right:20px;'>")


});s

