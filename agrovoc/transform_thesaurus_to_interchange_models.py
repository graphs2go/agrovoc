from collections.abc import Iterable

from graphs2go.models import interchange
from graphs2go.namespaces.skosxl import SKOSXL
from rdflib import SKOS, URIRef

from agrovoc.models.concept import Concept
from agrovoc.models.label import Label
from agrovoc.models.thesaurus import Thesaurus


def transform_thesaurus_to_interchange_models(
    thesaurus: Thesaurus,
) -> Iterable[interchange.Model]:
    for concept in thesaurus.concepts:
        yield interchange.Concept.builder(uri=concept.uri).build()

        for labels, predicate in (
            (concept.alt_label, SKOSXL.altLabel),
            (concept.pref_label, SKOSXL.prefLabel),
        ):
            for label in labels:
                if isinstance(label, Label):
                    yield interchange.Label.builder(
                        literal_form=label.literal_form,
                        predicate=predicate,
                        subject=concept.uri,
                        uri=label.uri,
                    ).build()
                else:
                    raise TypeError(label)

        for related_concepts, predicate in (
            (concept.broader, SKOS.broader),
            (concept.close_match, SKOS.closeMatch),
            (concept.exact_match, SKOS.exactMatch),
            (concept.related, SKOS.related),
        ):
            for related_concept in related_concepts:
                if isinstance(related_concept, Concept):
                    yield interchange.Relationship.builder(
                        object_=related_concept.uri,
                        predicate=predicate,
                        subject=concept.uri,
                    ).build()
                elif isinstance(related_concept, URIRef):
                    yield interchange.Relationship.builder(
                        object_=related_concept,
                        predicate=predicate,
                        subject=concept.uri,
                    ).build()
                else:
                    raise TypeError(related_concept)

        break
