import pystache
template = """@{{entry_type}}{ {{reference_name}},
title = "{{title}}",
author = {{#authors}}{{author}};{{/authors}},
{{#editors}}editor = {{editor}};{{/editors}}{{#editors}},{{/editors}}
{{#year}}year = {{year}},{{/year}}
{{#publisher}}publisher = {{publisher}},{{/publisher}}
{{#organization}}organization = {{organization}},{{/organization}}
{{#school}}school = {{school}},{{/school}}
{{#institution}}institution = {{institution}},{{/institution}}
{{#journal}}journal = {{journal}},{{/journal}}
{{#url}}url = {{url}},{{/url}}
{{#pages}}pages = {{pages}},{{/pages}}
{{#number}}number = {{number}},{{/number}}
{{#address}}address = {{address}},{{/address}}
{{#chapter}}chapter = {{chapter}},{{/chapter}}
{{#month}}month = {{month}},{{/month}}
{{#series}}series = {{series}},{{/series}}
{{#edition}}edition = {{edition}},{{/edition}}
{{#booktitle}}booktitle = {{booktitle}},{{/booktitle}}
{{#document}}document = {{document}},{{/document}}
}
"""

def create_bibitex(reference):
    authors = reference['authors']
    editors = reference['editors']
    
    reference['authors'] = [{'author': "%s, %s" % (author['lastname'], author['name']),} for author in authors]
    reference['editors'] = [{'editor':editor} for editor in editors]

    bibitex = pystache.render(template, reference)
    
    while '\n\n' in bibitex:
        bibitex = bibitex.replace('\n\n','\n')

    return bibitex

