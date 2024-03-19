from dagster import asset, get_dagster_logger
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from graphs2go.models import interchange
from rdflib import URIRef
from tqdm import tqdm

from agrovoc.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)
from agrovoc.models.release_graph import ReleaseGraph
from agrovoc.models.thesaurus import Thesaurus
from agrovoc.releases_partitions_definition import releases_partitions_definition


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph(
    rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph
) -> interchange.Graph.Descriptor:
    logger = get_dagster_logger()

    with interchange.Graph.create(
        rdf_store_config=rdf_store_config,
        identifier=URIRef(
            "urn:interchange:agrovoc-release:"
            + release_graph.release.version.isoformat()
        ),
    ) as interchange_graph:
        if not interchange_graph.is_empty:
            logger.info("interchange graph is not empty, skipping load")
            return interchange_graph.descriptor

        logger.info("loading interchange graph")

        thesaurus = Thesaurus(graph=release_graph.to_rdflib_graph())

        for model in tqdm(
            transform_thesaurus_to_interchange_models(thesaurus=thesaurus),
            desc="interchange models",
        ):
            interchange_graph.add(model)

        logger.info("loaded interchange graph")

        return interchange_graph.descriptor
