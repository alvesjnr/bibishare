from pyramid.security import Allow, Everyone

"""
	Bibishare authorization is the most simple possible: there are just one 
	security level which is 'logged'. It means that or you are logged in, or not.
	If you are logged in, you can edit documments and post messages. Else, you
	can't. But see, logged out users CAN create a new document.
"""

class Root(object):
    __acl__ = [ (Allow, 'logged', 'logged'),
              ]
    def __init__(self, request):
        pass