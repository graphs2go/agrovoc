from dagster import AssetExecutionContext, asset

from agrovoc.releases_partitions_definition import releases_partitions_definition
from agrovoc.models.release import Release


@asset(code_version="1", partitions_def=releases_partitions_definition)
def release(context: AssetExecutionContext) -> Release:
    return Release.from_partition_key(context.partition_key)
