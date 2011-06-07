import pystache
template = """@{{entry_type}}{ {{reference_name}},
title = "{{title}}",
author ={{#author}}{{author}}{{/author}},
{{#editor}}editor = {{editor}},{{/editor}}
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
	for key in reference:
		if isinstance(reference.get(key), list):
			as_dictionarie = [{key:value} for value in reference.get(key)]
			reference[key] = as_dictionarie
	bibitex = pystache.render(template, reference)
	return bibitex
