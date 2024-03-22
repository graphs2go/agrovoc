from datetime import datetime

from graphs2go.models import rdf
from rdflib import DCTERMS, RDF, Literal, URIRef


class Definition(rdf.Model):
    @property
    def created(self) -> datetime:
        return self._required_value(DCTERMS.created, self._map_term_to_datetime)

    @property
    def modified(self) -> datetime | None:
        return self._optional_value(DCTERMS.modified, self._map_term_to_datetime)

    @classmethod
    def primary_rdf_type(cls) -> URIRef:
        raise NotImplementedError

    @property
    def source(self) -> URIRef:
        return self._required_value(DCTERMS.source, self._map_term_to_uri)

    @property
    def value(self) -> Literal:
        return self._required_value(RDF.value, self._map_term_to_literal)
