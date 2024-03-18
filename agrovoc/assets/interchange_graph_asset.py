from dagster import asset
from rdflib import Graph

from agrovoc.models.release import Release
from agrovoc.models.thesaurus import Thesaurus
from agrovoc.releases_partitions_definition import releases_partitions_definition
from graphs2go.resources.interchange_config import InterchangeConfig


@asset(code_version="1", partitions_def=releases_partitions_definition)
def interchange_graph_asset(interchange_config: InterchangeConfig, release: Release):
    thesaurus = Thesaurus(graph=Graph().parse(source=release.nt_file_path))
