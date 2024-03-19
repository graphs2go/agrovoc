from agrovoc.assets.interchange_graph import interchange_graph
from graphs2go.models import interchange
from graphs2go.resources.oxigraph_config import OxigraphConfig

from agrovoc.models.release_graph import ReleaseGraph


def test_asset(oxigraph_config: OxigraphConfig, release_graph: ReleaseGraph) -> None:
    asset = interchange_graph(
        oxigraph_config=oxigraph_config, release_graph=release_graph
    )
    assert isinstance(asset, interchange.Graph.Descriptor)
    with interchange.Graph.open(descriptor=asset) as interchange_graph_:
        assert not interchange_graph_.is_empty
