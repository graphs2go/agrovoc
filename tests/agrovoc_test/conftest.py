from collections.abc import Iterable
import logging
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
logger = logging.getLogger(__name__)


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
    import oxrdflib  # noqa: F401

    graph = Graph(store="Oxigraph")
    oxigraph_dir_path = (
        oxigraph_config.parse(
            directory_path_default=Path(__file__).parent.parent.parent
            / "data"
            / "oxigraph"
        ).directory_path
        / "agrovoc"
        / release.version.isoformat()
    )
    oxigraph_dir_path.mkdir(parents=True, exist_ok=True)
    graph.open(str(oxigraph_dir_path))
    try:
        if len(graph) > 0:
            logger.info(
                "reuising existing Oxigraph %s with %d triples",
                oxigraph_dir_path,
                len(graph),
            )
        else:
            logger.info(
                "building %s Oxigraph from %s", oxigraph_dir_path, release.nt_file_path
            )
            graph.parse(source=release.nt_file_path)
            logger.info(
                "built %s Oxigraph from %s with %d triples",
                oxigraph_dir_path,
                release.nt_file_path,
                len(graph),
            )

        yield graph

        graph.close()
    finally:
        graph.close()


@pytest.fixture(scope="session")
def thesaurus(release_graph: Graph) -> Thesaurus:
    return Thesaurus(graph=release_graph)
