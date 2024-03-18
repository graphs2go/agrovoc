from collections.abc import Iterable
from rdflib import RDF, SKOS, Graph

from agrovoc.models.concept import Concept


class Thesaurus:
    def __init__(self, *, graph: Graph):
        self.__graph = graph

    @property
    def concepts(self) -> Iterable[Concept]:
        for uri in self.__graph.subjects(predicate=RDF.type, object=SKOS.Concept):
            yield Concept(resource=self.__graph.resource(uri))
