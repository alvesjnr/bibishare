from whoosh.index import open_dir, create_in
from whoosh import fields
import os

def normalize_name(names):
    def norm_one_name(name):
        name = dict(name)
        return "%s, %s;" % (name['lastname'],name['name'])

    return [norm_one_name(name) for name in names]


def create_index():

    schema = fields.Schema(title=fields.TEXT(stored=True), 
                           id=fields.ID(stored=True), 
                           authors=fields.TEXT(stored=True),
                           wiki=fields.TEXT,)

    if not os.path.exists("bibishare/search/index"):
        os.mkdir("bibishare/search/index")
    create_in("bibishare/search/index", schema)


def index(biblio):
    ix = open_dir("bibishare/search/index")
    writer = ix.writer()
    import pdb; pdb.set_trace()
    writer.add_document(title=biblio.title, 
                        wiki=biblio.wiki,
                        id=biblio._id, 
                        #authors=reduce(lambda a,b: "%s%s%s" % (a,' ',b), normalize_name(biblio["authors"])),
                        )

    writer.commit()

