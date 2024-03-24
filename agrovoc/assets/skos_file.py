from graphs2go.assets.build_skos_file_asset import build_skos_file_asset
from graphs2go.models import rdf

from agrovoc.releases_partitions_definition import releases_partitions_definition

skos_file = build_skos_file_asset(
    partitions_def=releases_partitions_definition,
    rdf_formats=(rdf.Format.NTRIPLES, rdf.Format.TURTLE),
)
