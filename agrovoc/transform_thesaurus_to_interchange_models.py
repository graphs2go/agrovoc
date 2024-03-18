from collections.abc import Iterable
from agrovoc.models.thesaurus import Thesaurus
from graphs2go.models import interchange


def transform_thesaurus_to_interchange_models(
    thesaurus: Thesaurus,
) -> Iterable[interchange.Model]:
    return ()
