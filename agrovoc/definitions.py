from dagster import Definitions
from graphs2go.resources import DirectoryInputConfig, OutputConfig, RdfStoreConfig
from graphs2go.utils import configure_markus, load_dotenv

from agrovoc.assets import (
    cypher_files,
    interchange_file,
    interchange_graph,
    release,
    release_graph,
    skos_file,
    skos_graph,
)
from agrovoc.jobs import files_job
from agrovoc.paths import DATA_DIRECTORY_PATH, INPUT_DIRECTORY_PATH

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        cypher_files,
        interchange_file,
        interchange_graph,
        release,
        release_graph,
        skos_file,
        skos_graph,
    ],
    jobs=[files_job],
    resources={
        "input_config": DirectoryInputConfig.from_env_vars(
            directory_path_default=INPUT_DIRECTORY_PATH
        ),
        "output_config": OutputConfig.from_env_vars(
            directory_path_default=DATA_DIRECTORY_PATH / "output"
        ),
        "rdf_store_config": RdfStoreConfig.from_env_vars(
            directory_path_default=DATA_DIRECTORY_PATH / "oxigraph"
        ),
    },
)
