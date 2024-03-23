from collections.abc import Iterable

from graphs2go.models import interchange, skos
from rdflib import SKOS

from agrovoc.models.concept import Concept
from agrovoc.models.label import Label
from agrovoc.models.thesaurus import Thesaurus


def __transform_labels(model: skos.LabeledModel) -> Iterable[interchange.Model]:
    for label_type, label in model.lexical_labels:
        assert isinstance(label, Label)
        yield interchange.Label.builder(
            literal_form=label.literal_form,
            subject=model,
            type_=label_type,
            uri=label.uri,
        ).set_created(label.created).set_modified(label.modified).build()


def transform_thesaurus_to_interchange_models(
    thesaurus: Thesaurus,
) -> Iterable[interchange.Model]:
    concept_scheme = thesaurus.concept_scheme
    yield interchange.Node.builder(uri=concept_scheme.uri).add_rdf_type(
        SKOS.ConceptScheme
    ).set_modified(concept_scheme.modified).build()
    yield from __transform_labels(concept_scheme)

    for concept in thesaurus.concepts:
        yield interchange.Node.builder(uri=concept.uri).add_rdf_type(
            SKOS.Concept
        ).set_created(concept.created).set_modified(concept.modified).build()
        yield from __transform_labels(concept)

        yield interchange.Relationship.builder(
            object_=concept_scheme, predicate=SKOS.inScheme, subject=concept
        ).build()

        for semantic_relation_predicate, related_concept in concept.semantic_relations:
            relationship_builder = interchange.Relationship.builder(
                object_=related_concept,
                predicate=semantic_relation_predicate,
                subject=concept,
            )
            if isinstance(related_concept, Concept):
                relationship_builder.set_created(related_concept.created).set_modified(
                    related_concept.modified
                )
            yield relationship_builder.build()
        break
