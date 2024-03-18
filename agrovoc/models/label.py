from datetime import datetime
from graphs2go.models.skos.label import Label as SkosLabel
from rdflib import DCTERMS, SKOS, Literal


class Label(SkosLabel):
    @property
    def created(self) -> datetime:
        return self._required_value(DCTERMS.created, self._map_term_to_datetime)

    # @property
    # def has_term_type(self) -> Iterable[Literal]:
    #     return self._values(
    #         AGRONTOLOGY.hasTermType,
    #         self._map_term_to_literal,
    #     )

    @property
    def modified(self) -> datetime | None:
        return self._optional_value(DCTERMS.modified, self._map_term_to_datetime)

    @property
    def notation(self) -> Literal:
        return self._required_value(SKOS.notation, self._map_term_to_literal)
