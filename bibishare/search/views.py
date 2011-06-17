from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import authenticated_userid
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')
from couchdbkit import ResourceNotFound



def basic_search(request):
	return Response('not yet implemented')