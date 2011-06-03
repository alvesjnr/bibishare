from models import Bibitex

import deform
import colander

class BibitexForm():

    base_schema = Bibitex.get_schema()
    base_schema['note'].widget = deform.widget.TextAreaWidget(cols=100, rows=25)
    @classmethod
    def get_form(cls):
        return deform.Form(cls.base_schema, buttons=('submit',))