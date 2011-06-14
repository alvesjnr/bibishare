from pyramid.config import Configurator
from bibishare.resources import Root
from pyramid.events import subscriber
from pyramid.events import NewRequest, NewResponse
from pyramid.i18n import get_localizer
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from .models import initialize_sql

import pyramid_zcml
import couchdbkit

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    config = Configurator(root_factory=Root, settings=settings)
    
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    maker = sessionmaker(bind=engine)
    settings['db.sessionmaker'] = maker

    config.scan('bibishare.models') # the "important" line
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    
    config.include(pyramid_zcml)
    config.load_zcml('configure.zcml')
 
    db_uri = settings['db_uri']
    conn = couchdbkit.Server(db_uri)
    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_couch_db, NewRequest)
    
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('static', 'bibishare:static')

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config.set_session_factory(my_session_factory)

    return config.make_wsgi_app()

def add_couch_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.couchdb = db
    
