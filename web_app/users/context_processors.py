from sport_site.utils import menu

def get_sport_context(request):
    return {'main_menu': menu}
