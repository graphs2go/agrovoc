from datetime import datetime

from returns.maybe import Maybe

from graphs2go.models import rdf
from rdflib import DCTERMS, RDF, Literal, URIRef


class Definition(rdf.Model):
    @property
    def created(self) -> Maybe[datetime]:
        return self.resource.optional_value(
            DCTERMS.created, rdf.Resource.ValueMappers.datetime
        )

    @property
    def modified(self) -> Maybe[datetime]:
        return self.resource.optional_value(
            DCTERMS.modified, rdf.Resource.ValueMappers.datetime
        )

    @classmethod
    def primary_rdf_type(cls) -> URIRef:
        raise NotImplementedError

    @property
    def source(self) -> Maybe[URIRef]:
        return self.resource.optional_value(
            DCTERMS.source, rdf.Resource.ValueMappers.iri
        )

    @property
    def value(self) -> Maybe[Literal]:
        return self.resource.optional_value(
            RDF.value, rdf.Resource.ValueMappers.literal
        )
