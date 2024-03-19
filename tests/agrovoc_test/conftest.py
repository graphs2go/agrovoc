from collections.abc import Iterable
import logging
from pathlib import Path
import oxrdflib
import pyoxigraph
import pytest
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.resources.oxigraph_config import OxigraphConfig
from graphs2go.utils.load_dotenv import load_dotenv
from rdflib import ConjunctiveGraph, Graph

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
def oxigraph_config() -> OxigraphConfig:
    return OxigraphConfig.default(
        directory_path_default=Path(__file__).parent.parent.parent / "data" / "oxigraph"
    )


@pytest.fixture(scope="session")
def release(release_config: ReleaseConfig) -> Release:
    return find_releases(release_config=release_config)[0]


@pytest.fixture(scope="session")
def release_config() -> ReleaseConfig:
    return ReleaseConfig.default()


@pytest.fixture(scope="session")
def release_graph(oxigraph_config: OxigraphConfig, release: Release) -> Iterable[Graph]:
    graph: Graph = (
        release_graph_asset(oxigraph_config=oxigraph_config, release=release)
    ).to_rdflib_graph()  # type: ignore

    try:
        yield graph
    finally:
        graph.close()


@pytest.fixture(scope="session")
def thesaurus(release_graph: Graph) -> Thesaurus:
    return Thesaurus(graph=release_graph)
