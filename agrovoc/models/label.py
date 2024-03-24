from datetime import datetime

from graphs2go.models import skos
from rdflib import DCTERMS


class Label(skos.Label):
    @property
    def created(self) -> datetime | None:
        return self._optional_value(DCTERMS.created, self._map_term_to_datetime)

    # @property
    # def has_term_type(self) -> Iterable[Literal]:
    #     return self._values(
    #         AGRONTOLOGY.hasTermType,
    #         self._map_term_to_literal,
    #     )

    @property
    def modified(self) -> datetime | None:
        return self._optional_value(DCTERMS.modified, self._map_term_to_datetime)
