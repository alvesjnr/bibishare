from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')
from textile import textile
from couchdbkit import ResourceNotFound

from models import Bibitex
from forms import BibitexForm

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def main(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    return {'main':main}


def new_entry(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    bibitex_form = BibitexForm.get_form()

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = bibitex_form.validate(controls)
        except deform.ValidationFailure, e:
            return render_to_response('bibitex:form.pt',
              {'form': e.render()})

        appstruct['wiki_as_html'] = textile(appstruct['wiki'])
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
            }

def view_biblio(request):
    main = get_renderer(BASE_TEMPLATE).implementation()
    try:
        bibitex = Bibitex.get(request.db, request.matchdict['id'])
    except ResourceNotFound:
    	return Response('404')
    return {'main':main,
            'bibitex':bibitex,
     		'wiki':bibitex.wiki_as_html}

