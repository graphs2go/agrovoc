from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class AGRONTOLOGY(DefinedNamespace):
    _NS = Namespace("http://aims.fao.org/aos/agrontology#")

    _fail = True

    # Properties
    isPartOfSubvocabulary: URIRef
    isProcessFor: URIRef
