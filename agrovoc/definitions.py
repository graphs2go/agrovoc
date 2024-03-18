from dagster import Definitions
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv

from agrovoc.assets.release import release
from agrovoc.resources.release_config import ReleaseConfig

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        release,
    ],
    resources={
        "release_config": ReleaseConfig.from_env_vars(),
    },
)
