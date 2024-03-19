import logging
from collections.abc import Iterable
from pathlib import Path

import pytest
from graphs2go.models import interchange
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv
from rdflib import Graph

from agrovoc.assets.interchange_graph import (
    interchange_graph as interchange_graph_asset,
)
from agrovoc.assets.release_graph import release_graph as release_graph_asset
from agrovoc.models.release import Release
from agrovoc.models.release_graph import ReleaseGraph
from agrovoc.models.thesaurus import Thesaurus
from agrovoc.resources.release_config import ReleaseConfig
from agrovoc.utils.find_releases import find_releases

load_dotenv()
configure_markus()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def interchange_graph(
    rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph
) -> interchange.Graph:
    descriptor: interchange.Graph.Descriptor = interchange_graph_asset(
        rdf_store_config=rdf_store_config, release_graph=release_graph
    )  # type: ignore
    return interchange.Graph.open(descriptor=descriptor)


@pytest.fixture(scope="session")
def rdf_store_config() -> RdfStoreConfig:
    return RdfStoreConfig.default(
        directory_path_default=Path(__file__).parent.parent.parent / "data" / "oxigraph"
    )


@pytest.fixture(scope="session")
def release(release_config: ReleaseConfig) -> Release:
    return find_releases(release_config=release_config)[0]


@pytest.fixture(scope="session")
def release_config() -> ReleaseConfig:
    return ReleaseConfig.default()


@pytest.fixture(scope="session")
def release_graph(rdf_store_config: RdfStoreConfig, release: Release) -> ReleaseGraph:
    return release_graph_asset(rdf_store_config=rdf_store_config, release=release)  # type: ignore


@pytest.fixture(scope="session")
def thesaurus(release_graph: Graph) -> Thesaurus:
    return Thesaurus(graph=release_graph)
