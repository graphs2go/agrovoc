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

from agrovoc.models.release import Release
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
    oxigraph_config_parsed = oxigraph_config.parse()
    assert oxigraph_config_parsed.directory_path
    oxigraph_dir_path = (
        oxigraph_config_parsed.directory_path / "agrovoc" / release.version.isoformat()
    )

    if oxigraph_dir_path.is_dir():
        logger.info("reusing existing Oxigraph %s", oxigraph_dir_path)
        store = pyoxigraph.Store(oxigraph_dir_path)
    else:
        oxigraph_dir_path.mkdir(parents=True, exist_ok=True)
        store = pyoxigraph.Store(oxigraph_dir_path)
        logger.info(
            "building %s Oxigraph from %s", oxigraph_dir_path, release.nt_file_path
        )
        # Use the underlying pyoxigraph bulk_load instead of going through rdflib, which is much slower
        store.bulk_load(release.nt_file_path, mime_type="application/n-triples")
        logger.info(
            "built %s Oxigraph from %s",
            oxigraph_dir_path,
            release.nt_file_path,
        )

    graph = ConjunctiveGraph(store=oxrdflib.OxigraphStore(store=store))
    try:
        yield graph
    finally:
        graph.close()


@pytest.fixture(scope="session")
def thesaurus(release_graph: Graph) -> Thesaurus:
    return Thesaurus(graph=release_graph)
