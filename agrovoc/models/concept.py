from collections.abc import Iterable

from graphs2go.models import skos
from rdflib import SKOS

from agrovoc.models.definition import Definition
from agrovoc.models.label import Label


class Concept(skos.Concept):
    _LABEL_CLASS = Label

    @property
    def definitions(self) -> Iterable[Definition]:
        """
        AGROVOC uses skos:definition to point to a custom shape rather than a literal, so it can add created/modified.
        """

        for iri in self._values(SKOS.definition, self._map_term_to_iri):
            yield Definition(resource=self.resource.graph.resource(iri))
