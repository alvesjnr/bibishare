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

from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.index import open_dir

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def get_user(request):
    userid = authenticated_userid(request)
    if userid:
        return request.dbsession.query(User).get(userid)

def basic_search(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    
    ix = open_dir("bibishare/search/index")

    q=request.GET.get('q')

    results = []
    
    if q:
        with ix.searcher() as searcher:
            query = MultifieldParser(["title", "wiki", "authors"], ix.schema).parse(q)
            results = searcher.search(query, limit=20)
            results = [dict(r.items()) for r in results]

    return {'main':main,
            'user':get_user(request),
            'results':results,
            }