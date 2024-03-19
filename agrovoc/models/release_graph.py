from dataclasses import dataclass
from pathlib import Path

import oxrdflib
import pyoxigraph
from rdflib import ConjunctiveGraph, Graph

from agrovoc.models.release import Release


@dataclass(frozen=True)
class ReleaseGraph:
    """
    Picklable descriptor of an rdflib.Graph containing an AGROVOC release.
    """

    oxigraph_directory_path: Path
    release: Release

    def to_rdflib_graph(self) -> Graph:
        """
        Get an rdflib Graph for this release graph.
        """

        return ConjunctiveGraph(
            store=oxrdflib.OxigraphStore(
                store=pyoxigraph.Store(self.oxigraph_directory_path)
            )
        )
