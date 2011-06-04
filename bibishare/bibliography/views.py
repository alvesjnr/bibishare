from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def main(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    return {'main':main}
