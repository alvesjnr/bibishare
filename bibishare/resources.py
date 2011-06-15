from pyramid.security import Allow, Everyone

class Root(object):
    __acl__ = [ (Allow, Everyone, 'everybody'),
                (Allow, 'basic', 'entry'),
                (Allow, 'secured', ('entry', 'topsecret'))
              ]
    def __init__(self, request):
        pass