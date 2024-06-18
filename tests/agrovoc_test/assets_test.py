from dagster import build_asset_context

from agrovoc.assets import cypher_files, interchange_graph, release_graph, skos_graph, releases_partitions_definition
from agrovoc.models import Release, ReleaseGraph
from graphs2go.models import interchange
from graphs2go.resources.output_config import OutputConfig
from graphs2go.resources.rdf_store_config import RdfStoreConfig


def test_cypher_files(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    output_config: OutputConfig,
) -> None:
    cypher_files(
        interchange_graph=interchange_graph_descriptor, output_config=output_config
    )  # type: ignore


def test_interchange_graph(rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph) -> None:
    asset = interchange_graph(
        rdf_store_config=rdf_store_config, release_graph=release_graph
    )
    assert isinstance(asset, interchange.Graph.Descriptor)
    with interchange.Graph.open(descriptor=asset, read_only=True) as interchange_graph_:
        assert not interchange_graph_.is_empty


def test_release() -> None:
    assert len(releases_partitions_definition.get_partition_keys()) > 0
    release(
        build_asset_context(
            partition_key=releases_partitions_definition.get_first_partition_key()
        )
    )

def test_release_graph(rdf_store_config: RdfStoreConfig, release: Release) -> None:
    asset = release_graph(rdf_store_config=rdf_store_config, release=release)
    assert isinstance(asset, ReleaseGraph.Descriptor)
    with ReleaseGraph.open(asset, read_only=True) as open_release_graph:
        assert not open_release_graph.is_empty


def test_skos_graph(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    rdf_store_config: RdfStoreConfig,
) -> None:
    skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
