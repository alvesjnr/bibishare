from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('bibishare')

from ..models import users

import datetime
import deform
import colander

class SignupForm():
    @classmethod
    def get_form(cls, localizer):
        
        def validate_username(node, value):
            msg = _("Username must not contains non alphanumeric digits",)
            if not value.isalnum():
                raise colander.Invalid(node, msg)
            
        class Schema(colander.Schema):
            username = colander.SchemaNode(
                colander.String(),
                #TODO create a validator
                validator=colander.All(validate_username),
                title=localizer.translate(_('Username')),
                description=localizer.translate(_('User name')),
            )
            password = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(min=5),
                widget=deform.widget.CheckedPasswordWidget(size=20),
                description=localizer.translate(_('Type your password and confirm it')),
            )
            email = colander.SchemaNode(
                colander.String(),
                validator=colander.Email(),
                title=localizer.translate(_('E-mail')),
                description=localizer.translate(_('Contact e-mail')),
            )
            __LOCALE__ = colander.SchemaNode(
                colander.String(),
                widget = deform.widget.HiddenWidget(),
                default= localizer.locale_name,
            )
        schema = Schema()

        return deform.Form(schema, buttons=('submit',))
