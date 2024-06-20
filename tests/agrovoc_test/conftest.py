import logging
from collections.abc import Iterable
from pathlib import Path

import pytest
from graphs2go.models import interchange, skos
from graphs2go.resources import DirectoryInputConfig, OutputConfig, RdfStoreConfig
from graphs2go.utils import configure_markus, load_dotenv
from returns.maybe import Some

from agrovoc import assets
from agrovoc.find_releases import find_releases
from agrovoc.models import Release, ReleaseGraph
from agrovoc.paths import INPUT_DIRECTORY_PATH, RDF_STORE_DIRECTORY_PATH

load_dotenv()
configure_markus()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def interchange_graph(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
) -> Iterable[interchange.Graph]:
    with interchange.Graph.open(
        descriptor=interchange_graph_descriptor, read_only=True
    ) as interchange_graph:
        yield interchange_graph


@pytest.fixture(scope="session")
def interchange_graph_descriptor(
    rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph
) -> interchange.Graph.Descriptor:
    return assets.interchange_graph(
        rdf_store_config=rdf_store_config, release_graph=release_graph
    )  # type: ignore


@pytest.fixture()
def output_config(tmp_path: Path) -> OutputConfig:
    return OutputConfig(directory_path=str(tmp_path))


@pytest.fixture(scope="session")
def rdf_store_config() -> RdfStoreConfig:
    return RdfStoreConfig.default(directory_path_default=Some(RDF_STORE_DIRECTORY_PATH))


@pytest.fixture(scope="session")
def release(input_config: DirectoryInputConfig) -> Release:
    return find_releases(input_config=input_config)[0]


@pytest.fixture(scope="session")
def input_config() -> DirectoryInputConfig:
    return DirectoryInputConfig.default(directory_path_default=INPUT_DIRECTORY_PATH)


@pytest.fixture(scope="session")
def release_graph(
    release_graph_descriptor: ReleaseGraph.Descriptor,
) -> Iterable[ReleaseGraph]:
    with ReleaseGraph.open(
        descriptor=release_graph_descriptor, read_only=True
    ) as release_graph:
        yield release_graph


@pytest.fixture(scope="session")
def release_graph_descriptor(
    rdf_store_config: RdfStoreConfig, release: Release
) -> ReleaseGraph.Descriptor:
    return assets.release_graph(rdf_store_config=rdf_store_config, release=release)  # type: ignore


@pytest.fixture(scope="session")
def skos_graph_descriptor(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    rdf_store_config: RdfStoreConfig,
) -> skos.Graph.Descriptor:
    return assets.skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
