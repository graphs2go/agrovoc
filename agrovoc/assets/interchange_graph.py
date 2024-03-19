from dagster import asset
from graphs2go.resources.oxigraph_config import OxigraphConfig
from rdflib import Graph

from agrovoc.models.release import Release
from agrovoc.models.thesaurus import Thesaurus
from agrovoc.releases_partitions_definition import releases_partitions_definition


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph_asset(oxigraph_config: OxigraphConfig, release: Release):
    thesaurus = Thesaurus(graph=Graph().parse(source=release.nt_file_path))

    for concept in thesaurus.concepts:
        pass
