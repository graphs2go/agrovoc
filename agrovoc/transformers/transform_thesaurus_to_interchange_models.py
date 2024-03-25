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

    for concept_i, concept in enumerate(thesaurus.concepts):
        # if concept_i == 100:
        #     break

        yield interchange.Node.builder(uri=concept.uri).add_rdf_type(
            SKOS.Concept
        ).set_created(concept.created).set_modified(concept.modified).build()

        yield from __transform_labels(concept)

        # concept, skos:inScheme, concept scheme
        yield interchange.Relationship.builder(
            object_=concept_scheme, predicate=SKOS.inScheme, subject=concept
        ).build()

        # Handle skos:definition specially since it's a subgraph and not a literal
        for definition in concept.definitions:
            definition_value = definition.value
            if definition_value is None:
                continue
            yield interchange.Property.builder(
                object_=definition_value,
                predicate=SKOS.definition,
                subject=concept,
                uri=definition.uri,
            ).set_created(definition.created).set_modified(
                definition.modified
            ).set_source(
                definition.source
            ).build()

        # skos:notation statements
        for notation in concept.notations:
            yield interchange.Property.builder(
                object_=notation, predicate=SKOS.notation, subject=concept
            ).build()

        # All skos:note sub-properties
        for note_predicate, note in concept.notes:
            yield interchange.Property.builder(
                object_=note, predicate=note_predicate, subject=concept
            ).build()

        # All skos:semanticRelation sub-properties
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
