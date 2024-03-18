from dagster import get_dagster_logger
from agrovoc.models.release import Release
from agrovoc.resources.release_config import ReleaseConfig
from graphs2go.utils.find_file_releases import find_file_releases


def find_releases(release_config: ReleaseConfig) -> tuple[Release, ...]:
    return find_file_releases(
        logger=get_dagster_logger(),
        release_directory_path=release_config.parse().directory_path,
        release_factory=Release,
    )
