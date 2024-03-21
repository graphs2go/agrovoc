import pytest
from graphs2go.models import interchange
from rdflib import Graph

from agrovoc.models.thesaurus import Thesaurus
from agrovoc.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)


def test_transform(thesaurus: Thesaurus) -> None:
    actual_interchange_model_class_set: set[type[interchange.Model]] = set()
    expected_interchange_model_class_set = {
        interchange.Concept,
        interchange.Label,
        interchange.Relationship,
    }
    interchange_graph = Graph()
    for interchange_model in transform_thesaurus_to_interchange_models(thesaurus):
        actual_interchange_model_class_set.add(interchange_model.__class__)
        interchange_graph += interchange_model.resource.graph
        if expected_interchange_model_class_set == actual_interchange_model_class_set:
            interchange_graph_ttl = interchange_graph.serialize(format="ttl")
            print(interchange_graph_ttl)
            return
    pytest.fail()
