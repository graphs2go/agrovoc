from collections.abc import Iterable
from rdflib import Graph


class Thesaurus:
    def __init__(self, *, graph: Graph):
        self.__graph = graph

    @property
    def concepts(self) -> Iterable[skos.Concept]:
        pass
