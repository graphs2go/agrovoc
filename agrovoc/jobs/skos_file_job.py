from dagster import define_asset_job

from agrovoc.assets.skos_file import skos_file as skos_file_asset

skos_file_job = define_asset_job(
    "skos_file_job", selection=["*" + skos_file_asset.key.path[0]]
)
