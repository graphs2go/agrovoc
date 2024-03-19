from collections.abc import Iterable
from pathlib import Path
import pytest
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.resources.oxigraph_config import OxigraphConfig
from graphs2go.utils.load_dotenv import load_dotenv
from rdflib import Graph

from agrovoc.models.release import Release
from agrovoc.models.thesaurus import Thesaurus
from agrovoc.resources.release_config import ReleaseConfig
from agrovoc.utils.find_releases import find_releases

load_dotenv()
configure_markus()


@pytest.fixture(scope="session")
def oxigraph_config() -> OxigraphConfig:
    return OxigraphConfig.default()


@pytest.fixture(scope="session")
def release(release_config: ReleaseConfig) -> Release:
    return find_releases(release_config=release_config)[0]


@pytest.fixture(scope="session")
def release_config() -> ReleaseConfig:
    return ReleaseConfig.default()


@pytest.fixture(scope="session")
def release_graph(oxigraph_config: OxigraphConfig, release: Release) -> Iterable[Graph]:
    import oxrdflib

    graph = Graph(store="Oxigraph")
    graph.open(
        str(oxigraph_config.parse().directory_path / release.version.isoformat())
    )
    try:
        if not graph:
            graph.parse(source=release.nt_file_path)

        yield graph

        graph.close()
    finally:
        graph.close()


@pytest.fixture(scope="session")
def thesaurus(release_graph: Graph) -> Thesaurus:
    return Thesaurus(graph=release_graph)
