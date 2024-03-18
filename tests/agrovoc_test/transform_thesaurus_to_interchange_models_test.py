import pytest
from graphs2go.models import interchange

from agrovoc.models.thesaurus import Thesaurus
from agrovoc.transform_thesaurus_to_interchange_models import (
    transform_thesaurus_to_interchange_models,
)


def test_transform(thesaurus: Thesaurus) -> None:
    actual_interchange_model_class_set: set[type[interchange.Model]] = set()
    expected_interchange_model_class_set = {interchange.Concept, interchange.Label}
    for interchange_model in transform_thesaurus_to_interchange_models(thesaurus):
        actual_interchange_model_class_set.add(interchange_model.__class__)
        if expected_interchange_model_class_set == actual_interchange_model_class_set:
            return
    pytest.fail()
