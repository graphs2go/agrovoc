from graphs2go.models import interchange
from graphs2go.resources.rdf_store_config import RdfStoreConfig

from agrovoc.assets.skos_graph import skos_graph


def test_asset(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    rdf_store_config: RdfStoreConfig,
) -> None:
    skos_graph(
        interchange_graph=interchange_graph_descriptor,
        rdf_store_config=rdf_store_config,
    )  # type: ignore
