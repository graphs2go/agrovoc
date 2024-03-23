from collections.abc import Iterable

from graphs2go.models import skos
from rdflib import SKOS

from agrovoc.models.definition import Definition
from agrovoc.models.label import Label


class Concept(skos.Concept):
    _LABEL_CLASS = Label

    @property
    def definition(self) -> Iterable[Definition]:
        for uri in self._values(SKOS.definition, self._map_term_to_uri):
            yield Definition(resource=self.resource.graph.resource(uri))

    # @property
    # def is_part_of_subvocabulary(self) -> Iterable[Literal]:
    #     return self._values(
    #         AGRONTOLOGY.isPartOfSubvocabulary,
    #         self._map_term_to_literal,
    #     )
