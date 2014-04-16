from uygulamatik import settings


def available_languages(request):
    return {'available_languages':settings.LANGUAGES}