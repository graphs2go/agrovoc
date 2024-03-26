from urllib.parse import quote

from dagster import asset, get_dagster_logger

from agrovoc.transformers.transform_release_graph_to_interchange_models import (
    transform_release_graph_to_interchange_models,
)
from graphs2go.models import interchange
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from rdflib import URIRef
from tqdm import tqdm

from agrovoc.models.release_graph import ReleaseGraph
from agrovoc.releases_partitions_definition import releases_partitions_definition


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph(
    rdf_store_config: RdfStoreConfig, release_graph: ReleaseGraph.Descriptor
) -> interchange.Graph.Descriptor:
    logger = get_dagster_logger()

    with interchange.Graph.create(
        rdf_store_config=rdf_store_config,
        identifier=URIRef("urn:interchange:" + quote(release_graph.identifier)),
    ) as open_interchange_graph:
        if not open_interchange_graph.is_empty:
            logger.info("interchange graph is not empty, skipping load")
            return open_interchange_graph.descriptor

        logger.info("loading interchange graph")

        open_interchange_graph.add_all(
            tqdm(
                transform_release_graph_to_interchange_models(release_graph),
                desc="interchange graph models",
            )
        )

        logger.info("loaded interchange graph")

        return open_interchange_graph.descriptor
