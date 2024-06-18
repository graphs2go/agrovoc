from dagster import define_asset_job

from agrovoc.assets import skos_file, interchange_file, cypher_files

files_job = define_asset_job(
    "files_job",
    selection=[
        "*" + cypher_files.key.path[0],
        "*" + interchange_file.key.path[0],
        "*" + skos_file.key.path[0],
    ],
)
