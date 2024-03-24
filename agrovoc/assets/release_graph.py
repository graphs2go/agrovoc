from dagster import asset, get_dagster_logger
from graphs2go.rdf_stores.rdf_store import RdfStore
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from rdflib import URIRef

from agrovoc.models.release import Release
from agrovoc.models.release_graph import ReleaseGraph
from agrovoc.releases_partitions_definition import releases_partitions_definition


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release_graph(rdf_store_config: RdfStoreConfig, release: Release) -> ReleaseGraph:
    logger = get_dagster_logger()

    with RdfStore.create(
        identifier=URIRef("urn:agrovoc-release:" + release.version.isoformat()),
        rdf_store_config=rdf_store_config,
    ) as rdf_store:
        if rdf_store.is_empty:
            logger.info(
                "building RDF store from %s",
                release.nt_file_path,
            )
            rdf_store.load(
                source=release.nt_file_path, mime_type="application/n-triples"
            )
            logger.info(
                "built RDF store from %s",
                release.nt_file_path,
            )
        else:
            logger.info("reusing existing RDF store")

        return ReleaseGraph(rdf_store_descriptor=rdf_store.descriptor, release=release)
