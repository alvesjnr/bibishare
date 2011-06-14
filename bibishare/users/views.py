from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')

from forms import SignupForm

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def login(request):
    return Response('login')

def logout(request):
    return Response('loghoout')

def signup(request):
    localizer = get_localizer(request)
    main = get_renderer(BASE_TEMPLATE).implementation()
    signup_form = SignupForm.get_form(localizer)

    if 'submit' in request.POST:
    	pass

    return {'main':main,
            'content':signup_form.render(),
            }
