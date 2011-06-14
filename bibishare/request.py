from pyramid.request import Request
from pyramid.decorator import reify

class MyRequest(Request):
    @reify
    def rel_db(self):
        maker = self.registry.settings['db.sessionmaker']
        return maker()