from agrovoc.assets.cypher_files import cypher_files
from graphs2go.models import interchange
from graphs2go.resources.output_config import OutputConfig


def test_asset(
    interchange_graph_descriptor: interchange.Graph.Descriptor,
    output_config: OutputConfig,
) -> None:
    cypher_files(
        interchange_graph=interchange_graph_descriptor, output_config=output_config
    )  # type: ignore
