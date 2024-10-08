from urllib.parse import quote

from dagster import (
    AssetExecutionContext,
    StaticPartitionsDefinition,
    asset,
    get_dagster_logger,
)
from graphs2go.assets import (
    build_cypher_files_asset,
    build_interchange_file_asset,
    build_skos_file_asset,
    build_skos_graph_asset,
)
from graphs2go.models import interchange
from graphs2go.rdf_stores import RdfStore
from graphs2go.resources import DirectoryInputConfig, RdfStoreConfig
from rdflib import URIRef
from returns.maybe import Some
from tqdm import tqdm

from agrovoc.find_releases import find_releases
from agrovoc.models import Release, Thesaurus
from agrovoc.paths import INPUT_DIRECTORY_PATH
from agrovoc.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)

# Static partitions: scan the release directory once at startup
releases_partitions_definition = StaticPartitionsDefinition(
    [
        release.to_partition_key()
        for release in find_releases(
            DirectoryInputConfig.from_env_vars(
                directory_path_default=INPUT_DIRECTORY_PATH
            )
        )
    ]
)


cypher_files = build_cypher_files_asset(
    partitions_def=Some(releases_partitions_definition)
)


interchange_file = build_interchange_file_asset(
    partitions_def=Some(releases_partitions_definition)
)


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph(
    rdf_store_config: RdfStoreConfig, thesaurus: Thesaurus.Descriptor
) -> interchange.Graph.Descriptor:
    with interchange.Graph.create(
        rdf_store_config=rdf_store_config,
        identifier=URIRef("urn:interchange:" + quote(thesaurus.identifier)),
    ) as open_interchange_graph:
        return open_interchange_graph.add_all_if_empty(
            lambda: tqdm(
                transform_thesaurus_to_interchange_models(thesaurus),
                desc="interchange graph models",
            )
        ).descriptor


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release(context: AssetExecutionContext) -> Release:
    return Release.from_partition_key(context.partition_key)


@asset(code_version="1", partitions_def=releases_partitions_definition)
def thesaurus(
    rdf_store_config: RdfStoreConfig, release: Release
) -> Thesaurus.Descriptor:
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

        return Thesaurus.Descriptor(
            identifier=release.identifier,
            rdf_store_descriptor=rdf_store.descriptor,
        )


skos_file = build_skos_file_asset(partitions_def=Some(releases_partitions_definition))


skos_graph = build_skos_graph_asset(partitions_def=Some(releases_partitions_definition))
