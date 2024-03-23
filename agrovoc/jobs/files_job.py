from dagster import define_asset_job

from agrovoc.assets.interchange_file import interchange_file as interchange_file_asset
from agrovoc.assets.skos_file import skos_file as skos_file_asset

files_job = define_asset_job(
    "file_job",
    selection=[
        "*" + interchange_file_asset.key.path[0],
        "*" + skos_file_asset.key.path[0],
    ],
)
