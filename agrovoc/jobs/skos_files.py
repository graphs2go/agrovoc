from dagster import define_asset_job

from agrovoc.assets.skos_files import skos_files as skos_files_asset

skos_files = define_asset_job(
    "skos_files", selection=["*" + skos_files_asset.key.path[0]]
)
