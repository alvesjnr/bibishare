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

import deform

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def get_user(request):
    userid = authenticated_userid(request)
    if userid:
        user = request.dbsession.query(User).get(userid)
    else:
        user = None
    return user

def main(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    userid = authenticated_userid(request)
    if userid:
        user = request.dbsession.query(User).get(userid)
    else:
        user = None

    return {'main':main,
            'user':get_user(request),
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
                   'form': e.render()}

        appstruct['bibitex'] = create_bibitex(appstruct.copy())

        if appstruct['wiki']:
            appstruct['wiki_as_html'] = textile(appstruct['wiki'])
        else:
            appstruct['wiki_as_html'] = ''

        bibitex = Bibitex.from_python(appstruct)
        bibitex.save(request.db)  

        return HTTPFound(location='/biblio/%s' % bibitex._id)

    else:
        if 'id' in request.matchdict: #edit
            bibitex = Bibitex.get(request.db, request.matchdict['id'])
            
            return {'main':main,
                    'form': bibitex_form.render(bibitex.to_python()),
                    }
    
    return {'main':main,
            'form':bibitex_form.render(),
            'user':get_user(request),
            }

def view_biblio(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    try:
        bibitex = Bibitex.get(request.db, request.matchdict['id'])
    except ResourceNotFound:
        return Response('404')

    return {'main':main,
            'bibitex':bibitex.to_python(),
            'reference':bibitex.bibitex,
            'wiki':bibitex.wiki_as_html,
            'user':get_user(request),
            }

