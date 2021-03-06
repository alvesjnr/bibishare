from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import authenticated_userid
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')
from textile import textile
from couchdbkit import ResourceNotFound

from sqlalchemy.orm.exc import NoResultFound

from models import Bibitex
from forms import BibitexForm
from bibitex import create_bibitex
from ..models.users import User
from ..search import indexer

from datetime import datetime

import deform

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def get_user(request):
    userid = authenticated_userid(request)
    if userid:
        return request.dbsession.query(User).get(userid)

def normalize_name(names):
    def norm_one_name(name):
        name = dict(name)
        return "%s, %s;" % (name['lastname'],name['name'])

    return [norm_one_name(name) for name in names]

def main(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    userid = authenticated_userid(request)
    
    last_entries = request.couchdb.view("couchapp/last", limit=200).all()

    last_entries = [ {'id':entry['id'], 
                      'title':entry['value'][0],
                      'authors':normalize_name(entry['value'][1]),
                      'publisher':entry['value'][2],
                     } for entry in last_entries]
    
    return {'main':main,
            'user':get_user(request),
            'articles':last_entries,
            }


def new_entry(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    bibitex_form = BibitexForm.get_form()

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = bibitex_form.validate(controls)
        except deform.ValidationFailure, e:
            return{'main':main,
                   'form': e.render(),
                   'user':get_user(request),
                   }

        bibitex = appstruct.copy()
        del(bibitex['document'])
        appstruct['bibitex'] = create_bibitex(bibitex)

        if appstruct['wiki']:
            appstruct['wiki_as_html'] = textile(appstruct['wiki'])
        else:
            appstruct['wiki_as_html'] = ''

        appstruct['modified_at'] = str(datetime.now())
        bibitex = Bibitex.from_python(appstruct)
        bibitex.save(request.couchdb)  
        indexer.index(bibitex._id,appstruct)

        return HTTPFound(location='/biblio/%s' % bibitex._id)

    else:
        if 'id' in request.matchdict: #edit
            bibitex = Bibitex.get(request.couchdb, request.matchdict['id'])
            
            return {'main':main,
                    'form': bibitex_form.render(bibitex.to_python()),
                    'user':get_user(request),
                    }
    
    return {'main':main,
            'form':bibitex_form.render(),
            'user':get_user(request),
            }

def view_biblio(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    try:
        bibitex = Bibitex.get(request.couchdb, request.matchdict['id'])
    
    except ResourceNotFound:
        return Response('404')
    try:
        document_url = bibitex.document['filename']
    except AttributeError:
        document_url = None
    
    metadata = bibitex.to_python()
    metadata['authors'] = normalize_name(metadata['authors'])

    return {'main':main,
            'metadata':metadata,
            'reference':bibitex.bibitex,
            'wiki':bibitex.wiki_as_html,
            'user':get_user(request),
            'download':document_url,
            }

def download(request):
    
    id = request.matchdict['id']
    filename = request.matchdict['filename']

    content_type = request.couchdb.get(id)['_attachments'][filename]['content_type']  
    document = request.couchdb.fetch_attachment(id,filename)

    return Response(body=document, content_type=content_type)
