from dataclasses import dataclass

from graphs2go.rdf_stores.rdf_store import RdfStore
from rdflib import ConjunctiveGraph, Graph

from agrovoc.models.release import Release


@dataclass(frozen=True)
class ReleaseGraph:
    """
    Picklable descriptor of an rdflib.Graph containing an AGROVOC release.
    """

    rdf_store_descriptor: RdfStore.Descriptor
    release: Release

    def to_rdflib_graph(self) -> Graph:
        """
        Get an rdflib Graph for this release graph.
        """

        return ConjunctiveGraph(store=RdfStore.open_(self.rdf_store_descriptor))
