from graphs2go.assets.build_interchange_file_asset import build_interchange_file_asset
from graphs2go.models import rdf

from agrovoc.releases_partitions_definition import releases_partitions_definition

interchange_file = build_interchange_file_asset(
    partitions_def=releases_partitions_definition,
    rdf_formats=(rdf.Format.NTRIPLES, rdf.Format.TURTLE),
)
