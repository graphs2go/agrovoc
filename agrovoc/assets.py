from urllib.parse import quote

from dagster import AssetExecutionContext, StaticPartitionsDefinition
from dagster import asset
from dagster import get_dagster_logger
from rdflib import URIRef
from tqdm import tqdm

from agrovoc.models.release import Release
from agrovoc.models.release_graph import ReleaseGraph
from agrovoc.resources import ReleaseConfig
from agrovoc.transform import transform
from graphs2go.assets.build_cypher_files_asset import build_cypher_files_asset
from graphs2go.assets.build_interchange_file_asset import build_interchange_file_asset
from graphs2go.assets.build_skos_file_asset import build_skos_file_asset
from graphs2go.assets.build_skos_graph_asset import build_skos_graph_asset
from graphs2go.models import interchange
from graphs2go.models import rdf
from graphs2go.rdf_stores.rdf_store import RdfStore
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from graphs2go.utils.find_file_releases import find_file_releases

# Static partitions: scan the release directory once at startup
releases_partitions_definition = StaticPartitionsDefinition(
    [
        release.to_partition_key()
        for release in find_file_releases(
            logger=get_dagster_logger(),
            release_directory_path=ReleaseConfig.from_env_vars().parse().directory_path,
            release_factory=Release,
        )
    ]
)


cypher_files = build_cypher_files_asset(
    partitions_def=releases_partitions_definition,
)


interchange_file = build_interchange_file_asset(
    partitions_def=releases_partitions_definition,
    rdf_formats=(rdf.Format.NTRIPLES, rdf.Format.TURTLE),
)


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph(
    rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph.Descriptor
) -> interchange.Graph.Descriptor:
    with interchange.Graph.create(
        rdf_store_config=rdf_store_config,
        identifier=URIRef("urn:interchange:" + quote(release_graph.identifier)),
    ) as open_interchange_graph:
        open_interchange_graph.add_all_if_empty(
            lambda: tqdm(
                transform(release_graph),
                desc="interchange graph models",
            )
        )
        return open_interchange_graph.descriptor


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release(context: AssetExecutionContext) -> Release:
    return Release.from_partition_key(context.partition_key)


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release_graph(
    rdf_store_config: RdfStoreConfig, release: Release
) -> ReleaseGraph.Descriptor:
    logger = get_dagster_logger()

    with RdfStore.create_(
        identifier=release.identifier,
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

        return ReleaseGraph.Descriptor(
            identifier=release.identifier,
            rdf_store_descriptor=rdf_store.descriptor,
        )


skos_file = build_skos_file_asset(
    partitions_def=releases_partitions_definition,
    rdf_formats=(rdf.Format.NTRIPLES, rdf.Format.TURTLE),
)


skos_graph = build_skos_graph_asset(partitions_def=releases_partitions_definition)
