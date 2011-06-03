from pyramid.config import Configurator
from bibishare.resources import Root
from pyramid.events import subscriber
from pyramid.events import NewRequest, NewResponse


import couchdbkit

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    config = Configurator(root_factory=Root, settings=settings)
 
    db_uri = settings['db_uri']
    conn = couchdbkit.Server(db_uri)
    config.registry.settings['db_conn'] = conn
    config.add_subscriber(add_couch_db, NewRequest) 
    
    return config.make_wsgi_app()

def add_couch_db(event):
    settings = event.request.registry.settings
    db = settings['db_conn'][settings['db_name']]
    event.request.db = db
    
