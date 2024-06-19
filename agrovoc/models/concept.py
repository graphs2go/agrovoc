from collections.abc import Iterable

from graphs2go.models import skos, rdf
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

        resource: rdf.NamedResource
        for resource in self.resource.values(
            SKOS.definition, rdf.Resource.ValueMappers.named_resource
        ):
            yield Definition(resource)
