from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')

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

def view_biblio(reques):
     main = get_renderer(BASE_TEMPLATE).implementation()
     return {'main':main,
     		'form':None}

