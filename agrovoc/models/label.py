from datetime import datetime

from returns.maybe import Maybe

from graphs2go.models import skos, rdf
from rdflib import DCTERMS


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
