from datetime import datetime

from graphs2go.models import rdf, skos
from rdflib import DCTERMS
from returns.maybe import Maybe


class Label(skos.Label):
    @property
    def created(self) -> Maybe[datetime]:
        return self.resource.optional_value(
            DCTERMS.created, rdf.Resource.ValueMappers.datetime
        )

    # @property
    # def has_term_type(self) -> Iterable[Literal]:
    #     return self._values(
    #         AGRONTOLOGY.hasTermType,
    #         self._map_term_to_literal,
    #     )

    @property
    def modified(self) -> Maybe[datetime]:
        return self.resource.optional_value(
            DCTERMS.modified, rdf.Resource.ValueMappers.datetime
        )
