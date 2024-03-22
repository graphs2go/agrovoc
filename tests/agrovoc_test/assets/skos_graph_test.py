from graphs2go.models import interchange
from graphs2go.resources.rdf_store_config import RdfStoreConfig

from agrovoc.assets.skos_graph import skos_graph
from agrovoc.assets.interchange_graph import (
    interchange_graph as interchange_graph_asset,
)
from agrovoc.models.release_graph import ReleaseGraph


def test_asset(rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph) -> None:
    interchange_graph_descriptor: (
        interchange.Graph.Descriptor
    ) = interchange_graph_asset(
        rdf_store_config=rdf_store_config, release_graph=release_graph
    )  # type: ignore

    skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
