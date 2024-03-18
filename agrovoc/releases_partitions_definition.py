from dagster import StaticPartitionsDefinition

from agrovoc.resources.release_config import ReleaseConfig
from agrovoc.utils.find_releases import find_releases

# Static partitions: scan the release directory once at startup
releases_partitions_definition = StaticPartitionsDefinition(
    [
        release.to_partition_key()
        for release in find_releases(ReleaseConfig.from_env_vars())
    ]
)
