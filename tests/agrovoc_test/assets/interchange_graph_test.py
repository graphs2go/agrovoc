from graphs2go.models import interchange
from graphs2go.resources.rdf_store_config import RdfStoreConfig

from agrovoc.assets.interchange_graph import interchange_graph
from agrovoc.models.release_graph import ReleaseGraph


def test_asset(rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph) -> None:
    asset = interchange_graph(
        rdf_store_config=rdf_store_config, release_graph=release_graph
    )
    assert isinstance(asset, interchange.Graph.Descriptor)
    with interchange.Graph.open(descriptor=asset) as interchange_graph_:
        assert not interchange_graph_.is_empty
