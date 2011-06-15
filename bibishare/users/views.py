from pyramid.view import view_config
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url, static_url
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.renderers import get_renderer
from pyramid.security import authenticated_userid
from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from forms import SignupForm, LoginForm
from ..models.users import User

from Crypto.Hash import SHA256

import deform

BASE_TEMPLATE = 'bibishare:templates/base.pt'

def get_user(request):
    userid = authenticated_userid(request)
    if userid:
        user = request.dbsession.query(User).get(userid)
    else:
        user = None
    return user

def login(request):
    FORM_TITLE = "Login"
    localizer = get_localizer(request)
    main = get_renderer(BASE_TEMPLATE).implementation()
    login_form = LoginForm.get_form(localizer)

    if 'submit' in request.POST:
        
        controls = request.POST.items()
        try:
            appstruct = login_form.validate(controls)
        except deform.ValidationFailure, e:
        
            return {'content':e.render(), 
                    'main':main, 
                    'form_title':FORM_TITLE,
                    'user':get_user(request),
                    }
        try:
            user = request.dbsession.query(User).filter_by(username=appstruct['username']).one()
        except NoResultFound:
            request.session.flash(u'Username doesnot exist.')
            return {'content':login_form.render(appstruct), 
                    'main':main, 
                    'form_title':FORM_TITLE,
                    'user':get_user(request),
                    }
        
        if SHA256.new(appstruct['password']).hexdigest() == user.password:
            headers = remember(request, user.id)
            return HTTPFound(location='/', headers=headers)
        else:
            request.session.flash(u'Username/password doesnot match.')
            return {'content':login_form.render(appstruct), 
                    'main':main, 
                    'form_title':FORM_TITLE,
                    'user':get_user(request),
                    }

    return {'user':get_user(request),
            'main':main,
            'content':login_form.render(),
            'form_title':FORM_TITLE,
            }

def logout(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)

def signup(request):

    FORM_TITLE = "Signup"
    localizer = get_localizer(request)
    main = get_renderer(BASE_TEMPLATE).implementation()
    signup_form = SignupForm.get_form(localizer)

    if 'submit' in request.POST:
        
        controls = request.POST.items()
        try:
            appstruct = signup_form.validate(controls)
        except deform.ValidationFailure, e:
        
            return {'content':e.render(), 
                    'main':main, 
                    'form_title':FORM_TITLE,
                    'user':get_user(request),
                    }
        del(appstruct['__LOCALE__'])
        user = User(**appstruct)
        request.dbsession.add(user)

        try:
           request.dbsession.commit()
        except IntegrityError:
           request.dbsession.rollback()
           request.session.flash(u'This username already exists.')
           return {'content':publisher_form.render(appstruct),
                   'main':main,
                   'form_title':FORM_TITLE,
                   'user':get_user(request),
                   }
        request.session.flash(u'User registered.')
        #TODO Login or not login?
        return HTTPFound(location=request.route_path('bibliography.main')) #TODO change to main portal

    return {'main':main,
            'content':signup_form.render(),
            'form_title':FORM_TITLE,
            'user':get_user(request),
            }
