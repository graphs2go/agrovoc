from graphs2go.resources.rdf_store_config import RdfStoreConfig

from agrovoc.assets.release_graph import release_graph
from agrovoc.models.release import Release
from agrovoc.models.release_graph import ReleaseGraph


def test_asset(rdf_store_config: RdfStoreConfig, release: Release) -> None:
    asset = release_graph(rdf_store_config=rdf_store_config, release=release)
    assert isinstance(asset, ReleaseGraph.Descriptor)
    with ReleaseGraph.open(asset, read_only=True) as open_release_graph:
        assert not open_release_graph.is_empty
