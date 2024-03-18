from dagster import Definitions
from graphs2go.resources.postgres_config import PostgresConfig
from graphs2go.resources.postgres_connection_pool import PostgresConnectionPool
from graphs2go.utils.configure_markus import configure_markus
from graphs2go.utils.load_dotenv import load_dotenv

from agrovoc.assets.concept_postgres_table import concept_postgres_table
from agrovoc.assets.concrete_value_postgres_table import concrete_value_postgres_table
from agrovoc.assets.description_postgres_table import description_postgres_table
from agrovoc.assets.language_refset_member_postgres_table import (
    language_refset_member_postgres_table,
)
from agrovoc.assets.postgres_database import postgres_database
from agrovoc.assets.postgres_schema import postgres_schema
from agrovoc.assets.postgres_tables import postgres_tables
from agrovoc.assets.relationship_postgres_table import relationship_postgres_table
from agrovoc.assets.release import release
from agrovoc.assets.release_type import release_type
from agrovoc.assets.skos_files import skos_files
from agrovoc.jobs.skos_job import skos_job
from agrovoc.resources.output_config import OutputConfig
from agrovoc.resources.release_config import ReleaseConfig

configure_markus()
load_dotenv()


definitions = Definitions(
    assets=[
        concept_postgres_table,
        concrete_value_postgres_table,
        description_postgres_table,
        language_refset_member_postgres_table,
        postgres_database,
        postgres_schema,
        postgres_tables,
        relationship_postgres_table,
        release,
        release_type,
        skos_files,
    ],
    jobs=[skos_job],
    resources={
        "output_config": OutputConfig.from_env_vars(),
        "postgres_connection_pool": PostgresConnectionPool.from_env_vars(),
        "postgres_config": PostgresConfig.from_env_vars(),
        "release_config": ReleaseConfig.from_env_vars(),
    },
)
