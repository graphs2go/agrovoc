from dagster import asset, get_dagster_logger
from graphs2go.resources.rdf_store_config import RdfStoreConfig
import pyoxigraph

from agrovoc.releases_partitions_definition import releases_partitions_definition
from agrovoc.models.release import Release
from agrovoc.models.release_graph import ReleaseGraph


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release_graph(rdf_store_config: RdfStoreConfig, release: Release) -> ReleaseGraph:
    logger = get_dagster_logger()

    oxigraph_config_parsed = rdf_store_config.parse()
    assert oxigraph_config_parsed.directory_path
    oxigraph_directory_path = (
        oxigraph_config_parsed.directory_path / "agrovoc" / release.version.isoformat()
    )

    if oxigraph_directory_path.is_dir():
        logger.info("reusing existing Oxigraph %s", oxigraph_directory_path)
    else:
        oxigraph_directory_path.mkdir(parents=True, exist_ok=True)
        store = pyoxigraph.Store(oxigraph_directory_path)
        logger.info(
            "building %s Oxigraph from %s",
            oxigraph_directory_path,
            release.nt_file_path,
        )
        # Use the underlying pyoxigraph bulk_load instead of going through rdflib, which is much slower
        store.bulk_load(release.nt_file_path, mime_type="application/n-triples")
        logger.info(
            "built %s Oxigraph from %s",
            oxigraph_directory_path,
            release.nt_file_path,
        )
        del store

    return ReleaseGraph(
        oxigraph_directory_path=oxigraph_directory_path, release=release
    )
