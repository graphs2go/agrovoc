from pathlib import Path
from dagster import Definitions
from graphs2go.resources.output_config import OutputConfig
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv

from agrovoc.assets.skos_files import skos_files
from agrovoc.assets.skos_graph import skos_graph
from agrovoc.assets.interchange_graph import interchange_graph
from agrovoc.assets.release import release
from agrovoc.assets.release_graph import release_graph
from agrovoc.jobs.skos_files_job import skos_files_job
from agrovoc.resources.release_config import ReleaseConfig

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        interchange_graph,
        release,
        release_graph,
        skos_files,
        skos_graph,
    ],
    jobs=[skos_files_job],
    resources={
        "output_config": OutputConfig.from_env_vars(
            directory_path_default=Path(__file__).parent.parent / "data" / "output"
        ),
        "rdf_store_config": RdfStoreConfig.from_env_vars(
            directory_path_default=Path(__file__).parent.parent / "data" / "oxigraph"
        ),
        "release_config": ReleaseConfig.from_env_vars(),
    },
)
