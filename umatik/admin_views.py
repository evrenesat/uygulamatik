#-*- coding:utf-8 -*-
import math
from json import dumps, loads
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.utils.translation import gettext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib import admin
from django.db.models import Q, Count
from umatik.models import *
from umatik.forms import UserRegistrationForm, LoginForm, PasswordChangeForm, InfoChangeForm
from umatik.helpers import create_app, node_validation
from django.utils.translation import ugettext_lazy as _


def main(request):
    """
    Anasayfa
    @return: null
    """
    return HttpResponse('', mimetype="application/json")


@staff_member_required
def index(request):
    if request.user.is_superuser:
        return admin.site.index(request)
    else:
        return HttpResponseRedirect("/admin/")


def home_user(request):
    """
    uygulama sahibi kullanicilarin anasayfasi
    """
    if request.user.is_superuser:
        return admin.site.index(request)

    login_form = LoginForm()
    registration_form = UserRegistrationForm()
    if request.POST:
        # app yaratma
        if 'app_submit' in request.POST:
            if 'app_type' not in request.POST or not len(request.POST['app_name']):
                messages.error(request, u"Uygulama tipini ve adını eksiksiz giriniz.")
            else:
                if request.user.is_authenticated():
                    app = create_app(request.user, request.POST['app_type'], request.POST['app_name'])
                    request.session["appid"] = app.id
                    request.session["subd"] = app.subdomain
                    return HttpResponseRedirect("/admin/application_details/" + str(app.id))
                else:
                    request.session['app_type'] = request.POST['app_type']
                    request.session['app_name'] = request.POST['app_name']
                    return HttpResponseRedirect('/admin/user_registration/')

        # kullanici girisi
        elif 'login_submit' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user_auth = authenticate(username = login_form.cleaned_data['email'],
                                password = login_form.cleaned_data['password'])
                if user_auth:
                    login(request, user_auth)
                    if request.user.is_superuser:
                        return admin.site.index(request)
                    else:
                        return HttpResponseRedirect('/admin')
                else:
                    messages.error(request, gettext('E-Mail or password incorrect.'))


    try:
        profile = request.user.profile
    except Exception:
        profile = None
    context = {
        'avail_apptypes': AppType.objects.all(),
        'avail_apps': request.user.profile.apps.all() if profile else [],
        'login_form': login_form,
        'registration_form': registration_form
    }
    return render_to_response('admin/user_appselect.html', context, RequestContext(request))


def user_registration(request):
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            tmp_arr = form.cleaned_data['email'].split('@')
            usrname = tmp_arr[0]
            user = User.objects.create_user(usrname,
                    form.cleaned_data['email'], form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            group = Group.objects.get(name='is_an_app_admin')
            group.user_set.add(user)
            app = create_app(user, request.session['app_type'], request.session['app_name'])
            request.session["appid"] = app.id
            request.session["subd"] = app.subdomain
            del request.session['app_type']
            del request.session['app_name']
            user_auth = authenticate(username = form.cleaned_data['email'],
                        password = form.cleaned_data['password'])
            if user_auth:
                login(request, user_auth)
                # TODO : kullaniciya eposta atilacak
                return HttpResponseRedirect("/admin/application_details/" + str(app.id))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render_to_response('admin/user_registration.html', context, RequestContext(request))


@staff_member_required
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(request.POST, request=request)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, gettext('Your password has been changed successfully.'))
            return HttpResponseRedirect('/admin/change_password')
    else:
        form = PasswordChangeForm(request=request)
    context = {
        'form': form,
        'title': _('Change password')
    }
    return render_to_response('admin/change_password.html', context, RequestContext(request))



@staff_member_required
def get_icon(request, id):
    return HttpResponse(Icon.objects.filter(pk=id).values_list('image', flat=True), 'text/plain')

@staff_member_required
def change_info(request):
    form_initial = {
        'name': request.user.first_name,
        'surname': request.user.last_name,
        'email': request.user.email
    }
    if request.POST:
        form = InfoChangeForm(request.POST, initial=form_initial)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['surname']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, gettext('Your personal info has been changed successfully.'))
            return HttpResponseRedirect('/admin/change_info')
    else:
        form = InfoChangeForm(initial=form_initial)
    context = {
        'form': form,
        'title': _('Update user info')
    }
    return render_to_response('admin/change_info.html', context, RequestContext(request))



@staff_member_required
def application_details(request, id):
    app = Application.objects.select_related("type").get(pk=id)
    if not request.user.is_superuser:
        assert request.user.id == app.profile_set.all()[0].user.id, "Yetkisiz giris denemesi"
    request.session["appid"] = app.id
    request.session["subd"] = app.subdomain
    context = {
        "app_template": "admin/app/" + app.type.codename + ".html",
        'app': app
    }
    return render_to_response("admin/index.html", context, RequestContext(request))


@staff_member_required
def home(request):
    """
    yonetici anasayfasi
    """
    assert request.user.is_superuser, "Yetkisiz giris denemesi"
    if request.POST:
        if not request.POST["app_type"] or not request.POST["app_name"]:
            messages.error(request, u"Uygulama tipini ve adını eksiksiz giriniz.")
        else:
            app = create_app(request)
            return HttpResponseRedirect("/admin/umatik/application/" + str(app.id))
    elif request.GET.get('appid'):
        # request.session["appid"] = request.GET['appid']
        # request.session["subd"] = app.subdomain
        return HttpResponseRedirect("/admin/umatik/application/%s" % request.GET['appid'])
    context = {
        'avail_apptypes': AppType.objects.all(),
        'avail_apps': Application.objects.all(),
    }
    return render_to_response('admin/appselect.html', context, context_instance=RequestContext(request))


@staff_member_required
def map(request):
    nodes = Place.objects.filter(x__isnull=False)
    return render_to_response('admin/map.html',
                              {'nodes': nodes},
                              context_instance=RequestContext(request)
    )


@staff_member_required
@csrf_exempt
def get_app_map(request):
    request.session["map_id"] = request.POST["mapId"]
    map = Map.objects.get(app_id=request.session["appid"], id=request.POST['mapId'])
    result = {
        "status": "ok",
        "map": str(map.map.url),
        "app_id": request.session["appid"],
        "map_id": request.POST["mapId"]
    }
    return HttpResponse(dumps(result))


@staff_member_required
def right_click_context(request):
    return render_to_response("admin/inc/right_click_context.html", {}, RequestContext(request))


from umatik.models import NODE_TYPES


@staff_member_required
@csrf_exempt
def get_node_form(request):
    nodes = Node.objects.filter(app_id=request.session['appid'])
    context = {
        "types": NODE_TYPES,
        "nodes": nodes
    }
    return render_to_response("admin/inc/node_form.html", context, RequestContext(request))


@staff_member_required
def get_nodes(request):
    nodes = Node.objects.filter(app_id=request.session["appid"], map_id=request.session['map_id']).annotate(
        n_count=Count('frm'))
    nodes_formatted = list()
    for node in nodes:
        nodes_formatted.append({
            'id': node.id,
            'x': node.x,
            'y': node.y,
            'n_count': node.n_count
        })
    return HttpResponse(dumps(nodes_formatted))


@staff_member_required
@csrf_exempt
def add_node(request):
    data = loads(request.raw_post_data)
    node = data["node"]

    # validation
    val_result = node_validation(node)
    if val_result['status'] == 'error':
        return HttpResponse(dumps(val_result))


    app = Application.objects.get(pk=request.session['appid'])
    map = Map.objects.get(pk=request.session['map_id'])
    try:
        node_obj = Node(
            app=app,
            map=map,
            type=int(node["type"]),
            name=node["name"],
            x=int(node["x"]),
            y=int(node["y"])
        )
        node_obj.save()
    except Exception:
        result = {
            "status": "error",
            "message": gettext("Kayit sirasinda hata olustu! Yeniden deneyiniz.")
        }
        return HttpResponse(dumps(result))

    # store ya da exhibitor verisi olmasi durumunda bu node'la baglantisini saglamak
    if "store" in node:
        Place.objects.filter(pk=int(node["store"])).update(node=node_obj)
    if "exhibitor" in node:
        Exhibitor.objects.filter(pk=int(node["exhibitor"])).update(node=node_obj)

    result = {
        "status": "ok",
        "message": gettext("Kayit islemi basarili."),
        "node_id": node_obj.id
    }
    return HttpResponse(dumps(result))


@staff_member_required
def delete_node(request, id):
    try:
        node = Node.objects.get(pk=id)
        Place.objects.filter(node=node).update(node=None)
        Exhibitor.objects.filter(node=node).update(node=None)
        node.delete()
        result = {
            "status": "ok",
            "message": gettext("Silme islemi basarili")
        }
    except Exception:
        result = {
            "status": "error",
            "message": gettext("Silme islemi sirasinda hata olustu! Lutfen yeniden deneyin.")
        }
    return HttpResponse(dumps(result))


@staff_member_required
def get_store_list(request):
    stores = Place.objects.filter(app_id=request.session['appid'], node=None)
    return render_to_response("admin/inc/store_list.html", {"stores": stores}, RequestContext(request))


@staff_member_required
def get_exhibitor_list(request):
    exhibitors = Exhibitor.objects.filter(app_id=request.session['appid'], node=None)
    template = "admin/inc/exhibitor_list.html"
    return render_to_response(template, {"exhibitors": exhibitors}, RequestContext(request))


@staff_member_required
def get_node_update_form(request, id):
    node = Node.objects.get(pk=id)
    nodes = Node.objects.filter(~Q(id=id), app_id=request.session['appid'])

    try:
        store = Place.objects.get(node=node)
        store_id = store.id
    except Exception:
        store_id = None
    stores = None
    if store_id:
        stores = Place.objects.filter(Q(node=None) | Q(node=node), app_id=request.session['appid'])

    try:
        exhibitor = Exhibitor.objects.get(node=node)
        exhibitor_id = exhibitor.id
    except Exception:
        exhibitor_id = None
    exhibitors = None
    if exhibitor_id:
        exhibitors = Exhibitor.objects.filter(Q(node=None) | Q(node=node), app_id=request.session['appid'])

    context = {
        "node": node,
        "store_id": store_id,
        "exhibitor_id": exhibitor_id,
        "types": NODE_TYPES,
        "nodes": nodes,
        "stores": stores,
        "exhibitors": exhibitors
    }
    template = "admin/inc/node_update_form.html"
    return render_to_response(template, context, RequestContext(request))


@staff_member_required
@csrf_exempt
def update_node(request):
    data = loads(request.raw_post_data)
    node = data["node"]

    # validation
    # validation
    val_result = node_validation(node)
    if val_result['status'] == 'error':
        return HttpResponse(dumps(val_result))


    try:
        Node.objects.filter(pk=node["nodeId"], app_id=request.session['appid']).update(type=int(node["type"]),
                                                                                       name=node["name"])
        node_obj = Node.objects.get(pk=int(node["nodeId"]))
    except Exception:
        result = {
            "status": "error",
            "message": gettext("Node guncellemede hata meydana geldi.")
        }
        return HttpResponse(dumps(result))

    # store ekleme, guncelleme, silme
    if "store" in node:
        if "previousStore" in node:
            if node["previousStore"] != node["store"]:
                Place.objects.filter(node=node_obj).update(node=None)
                Place.objects.filter(id=int(node["store"])).update(node=node_obj)
        else:
            Place.objects.filter(id=int(node["store"])).update(node=node_obj)
    else:
        if "previousStore" in node:
            Place.objects.filter(node=node_obj).update(node=None)

    # exhibitor ekleme, guncelleme, silme
    if "exhibitor" in node:
        if "previousExhibitor" in node:
            if node["previousExhibitor"] != node["exhibitor"]:
                Exhibitor.objects.filter(node=node_obj).update(node=None)
                Exhibitor.objects.filter(id=int(node["exhibitor"])).update(node=node_obj)
        else:
            Exhibitor.objects.filter(id=int(node["exhibitor"])).update(node=node_obj)
    else:
        if "previousExhibitor" in node:
            Exhibitor.objects.filter(node=node_obj).update(node=None)

    result = {
        "status": "ok",
        "message": gettext("Guncelleme islemi basarili")
    }
    return HttpResponse(dumps(result))


@staff_member_required
@csrf_exempt
def get_neighbours(request):
    node = Node.objects.get(pk=request.POST['nodeId'])
    neighbours = Matrix.objects.select_related('node2').filter(node1=node).values('node2__id', 'node2__name',
                                                                                  'node2__x', 'node2__y')
    result = {
        'frm': {'id': node.id, 'name': node.name, 'x': node.x, 'y': node.y},
        'to': list()
    }
    for i in neighbours:
        result['to'].append({
            'id': i['node2__id'], 'name': i['node2__name'], 'x': i['node2__x'], 'y': i['node2__y']
        })
    return HttpResponse(dumps(result))

@never_cache
def get_defaults(request):
    app = Application.objects.get(pk=request.GET['aid'])
    out = """
    document.theme = '{jquery_theme}';
    """
    data = {
        'jquery_theme': app.jmt
    }
    return HttpResponse(out.format(**data), 'application/javascript')


@staff_member_required
def add_neighbour(request, frm, to):
    node1 = Node.objects.get(pk=frm)
    node2 = Node.objects.get(pk=to)
    matrix = Matrix.objects.filter(Q(node1_id=frm, node2_id=to) | Q(node1_id=to, node2_id=frm))
    if matrix.count():
#        matrix.delete()
        Matrix.objects.filter(Q(node1_id=frm, node2_id=to) | Q(node1_id=to, node2_id=frm)).delete()
        result = {
            'frm': frm,
            'to': to,
            'status': 'delete',
            'message': gettext(node1.name + ' ile ' + node2.name + ' arasindaki komsuluk silindi.')
        }
    else:
        distance = math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
        m = Matrix(
            app_id=request.session['appid'],
            node1=node1,
            node2=node2,
            distance=distance
        )
        m.save()
        result = {
            'frm': frm,
            'to': to,
            'status': 'add',
            'message': gettext(node1.name + ' ile ' + node2.name + ' arasinda komsuluk kuruldu.')
        }

    return HttpResponse(dumps(result))





