from pathlib import Path

from dagster import Definitions
from graphs2go.resources.output_config import OutputConfig
from graphs2go.resources.rdf_store_config import RdfStoreConfig
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv

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
from agrovoc.resources import ReleaseConfig

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
        "output_config": OutputConfig.from_env_vars(
            directory_path_default=Path(__file__).parent.parent / "data" / "output"
        ),
        "rdf_store_config": RdfStoreConfig.from_env_vars(
            directory_path_default=Path(__file__).parent.parent / "data" / "oxigraph"
        ),
        "release_config": ReleaseConfig.from_env_vars(),
    },
)
