#-*- coding:utf8 -*-
from django.utils.translation import gettext
from umatik.models import Application, Theme, AppType, Profile


def create_app(user, app_type, app_name):
    app = Application(
        type=AppType.objects.get(pk=app_type),
        theme=Theme.objects.all()[0],
        name_short = app_name
    )
    app.save()
    app.createModuleSelections()
    try:
        profile = user.profile
    except Exception:
        profile = Profile(user = user)
        profile.save()
    profile.apps.add(app)
    return app


def node_validation(node):
    result = {'status':'ok'}

    if len(node['name']) > 30:
        result = {
            'status': 'error',
            'message': gettext('Name of the node should not be longer than 30 characters.')
        }

    if not node['type']:
        result = {
            'status': 'error',
            'message': gettext('You must choose a node type.')
        }
    return result