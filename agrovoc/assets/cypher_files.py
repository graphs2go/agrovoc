from graphs2go.assets.build_cypher_files_asset import build_cypher_files_asset

from agrovoc.releases_partitions_definition import releases_partitions_definition

cypher_files = build_cypher_files_asset(
    partitions_def=releases_partitions_definition,
)
