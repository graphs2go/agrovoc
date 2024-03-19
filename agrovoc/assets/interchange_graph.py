from dagster import asset, get_dagster_logger
from graphs2go.resources.oxigraph_config import OxigraphConfig
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
    oxigraph_config: OxigraphConfig, release_graph: ReleaseGraph
) -> interchange.Graph.Descriptor:
    logger = get_dagster_logger()

    with interchange.Graph.create(
        oxigraph_config=oxigraph_config,
        identifier=URIRef("http://aims.fao.org/aos/agrovoc/"),
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
