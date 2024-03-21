from dagster import define_asset_job

from agrovoc.assets.skos_files import skos_files as skos_files_asset

skos_files_job = define_asset_job(
    "skos_files_job", selection=["*" + skos_files_asset.key.path[0]]
)
