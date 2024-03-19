from dagster import asset
from graphs2go.resources.oxigraph_config import OxigraphConfig
from graphs2go.models import interchange
from rdflib import URIRef

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
    with interchange.Graph.create(
        oxigraph_config=oxigraph_config,
        identifier=URIRef("http://aims.fao.org/aos/agrovoc/"),
    ) as interchange_graph:
        thesaurus = Thesaurus(graph=release_graph.to_rdflib_graph())

        for model in transform_thesaurus_to_interchange_models(thesaurus=thesaurus):
            interchange_graph.add(model)

        return interchange_graph.descriptor
