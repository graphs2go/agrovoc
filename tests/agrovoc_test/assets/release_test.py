from dagster import build_asset_context

from agrovoc.assets.release import release
from agrovoc.releases_partitions_definition import releases_partitions_definition


def test_asset() -> None:
    assert len(releases_partitions_definition.get_partition_keys()) > 0
    release(
        build_asset_context(
            partition_key=releases_partitions_definition.get_first_partition_key()
        )
    )
