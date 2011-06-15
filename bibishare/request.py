from pyramid.request import Request
from pyramid.decorator import reify

class MyRequest(Request):
    @reify
    def dbsession(self):
        maker = self.registry.settings['rel_db.sessionmaker']
        return maker()