from isis import model
import deform

choices = ['article', 'book', 'booklet', 'conference', 'inbook', 'incollection', 'inproceedings',
           'manual', 'mastersthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished', ]


class Bibitex(model.CouchdbDocument):
    entry_type = model.TextProperty(choices=[(entry,entry) for entry in choices],)
    reference_name = model.TextProperty(required=True) #name which will be used in \cite{}

    title = model.TextProperty(required=True)
    authors = model.MultiCompositeTextProperty(required=True, subkeys=['name', 'lastname'])
    publisher = model.TextProperty()
    editor = model.MultiTextProperty()
    chapter = model.TextProperty()
    year = model.TextProperty()
    note = model.TextProperty()
    address = model.TextProperty()
    url = model.TextProperty()
    volume = model.TextProperty()
    number = model.TextProperty()
    series = model.MultiTextProperty()
    school = model.TextProperty()
    pages = model.TextProperty()
    organization = model.TextProperty()
    institution = model.TextProperty()
    month = model.TextProperty()
    journal = model.TextProperty()
    edition = model.TextProperty()
    crossref = model.TextProperty()
    booktitle = model.TextProperty()
    annote = model.TextProperty()


"""
    -address: Publisher's address (usually just the city, but can be the full address for lesser-known publishers)
    -annote: An annotation for annotated bibliography styles (not typical)
    -author: The name(s) of the author(s) (in the case of more than one author, separated by and)
    -booktitle: The title of the book, if only part of it is being cited
    -chapter: The chapter number
    -crossref: The key of the cross-referenced entry
    -edition: The edition of a book, long form (such as "first" or "second")
    -editor: The name(s) of the editor(s)
    -institution: The institution that was involved in the publishing, but not necessarily the publisher
    -journal: The journal or magazine the work was published in
    -month: The month of publication (or, if unpublished, the month of creation)
    -note: Miscellaneous extra information
    -number: The "(issue) number" of a journal, magazine, or tech-report, if applicable. (Most publications have a "volume", but no "number" field.)
    -organization: The conference sponsor
    -pages: Page numbers, separated either by commas or double-hyphens.
    -publisher: The publisher's name
    -school: The school where the thesis was written
    -series: The series of books the book was published in (e.g. "The Hardy Boys" or "Lecture Notes in Computer Science")
    -title: The title of the work
    -type: The type of tech-report, for example, "Research Note"
    -url: The WWW address
    -volume: The volume of a journal or multi-volume book
    -year: The year of publication (or, if unpublished, the year of creation)
"""

