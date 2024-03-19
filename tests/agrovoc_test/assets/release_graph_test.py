import pytest
from agrovoc.assets.release_graph import release_graph
from agrovoc.models.release import Release
from graphs2go.resources.oxigraph_config import OxigraphConfig

from agrovoc.models.release_graph import ReleaseGraph


def test_asset(oxigraph_config: OxigraphConfig, release: Release) -> None:
    asset = release_graph(oxigraph_config=oxigraph_config, release=release)
    assert isinstance(asset, ReleaseGraph)
    graph = asset.to_rdflib_graph()
    for _ in graph.triples((None, None, None)):
        return
    pytest.fail()
