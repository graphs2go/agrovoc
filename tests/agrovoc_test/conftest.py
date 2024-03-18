import pytest
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv
from agrovoc.resources.release_config import ReleaseConfig
from agrovoc.models.release import Release
from agrovoc.utils.find_releases import find_releases

load_dotenv()
configure_markus()


@pytest.fixture(scope="session")
def release(release_config: ReleaseConfig) -> Release:
    return find_releases(release_config=release_config)[0]


@pytest.fixture(scope="session")
def release_config() -> ReleaseConfig:
    return ReleaseConfig.default()
