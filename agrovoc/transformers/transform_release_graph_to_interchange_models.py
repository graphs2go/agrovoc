from collections.abc import Iterable

from graphs2go.models import interchange, skos
from rdflib import SKOS, URIRef

from agrovoc.models.concept import Concept
from agrovoc.models.label import Label
from agrovoc.models.release_graph import ReleaseGraph

_CONCEPT_BATCH_SIZE = 100


def __transform_labels(model: skos.LabeledModel) -> Iterable[interchange.Model]:
    for label_type, label in model.lexical_labels:
        assert isinstance(label, Label)
        yield interchange.Label.builder(
            literal_form=label.literal_form,
            subject=model,
            type_=label_type,
            uri=label.uri,
        ).set_created(label.created).set_modified(label.modified).build()


def __transform_concept(
    *, concept: Concept, concept_scheme_uri: URIRef
) -> Iterable[interchange.Model]:
    yield interchange.Node.builder(uri=concept.uri).add_rdf_type(
        SKOS.Concept
    ).set_created(concept.created).set_modified(concept.modified).build()

    yield from __transform_labels(concept)

    # concept, skos:inScheme, concept scheme
    yield interchange.Relationship.builder(
        object_=concept_scheme_uri, predicate=SKOS.inScheme, subject=concept
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
        ).set_created(definition.created).set_modified(definition.modified).set_source(
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


# def _transform_concept_consumer(
#     input_: tuple[URIRef, ReleaseGraph.Descriptor],
#     output_queue: Queue,
#     work_queue: JoinableQueue,
# ) -> None:
#     (concept_scheme_uri, release_graph_descriptor) = input_
#
#     with ReleaseGraph.open(release_graph_descriptor, read_only=True) as release_graph:
#         while True:
#             concept_uris: tuple[URIRef, ...] | None = work_queue.get()
#
#             if concept_uris is None:
#                 work_queue.task_done()
#                 break  # Signal from the producer there's no more work
#
#             interchange_models: list[interchange.Model] = []  # type: ignore
#             for concept_uri in concept_uris:
#                 interchange_models.extend(
#                     __transform_concept(
#                         concept_scheme_uri=concept_scheme_uri,
#                         concept=release_graph.concept_by_uri(concept_uri),
#                     )
#                 )
#             output_queue.put(tuple(interchange_models))
#             work_queue.task_done()
#
#
# def _transform_concept_producer(
#     input_: ReleaseGraph.Descriptor, work_queue: JoinableQueue
# ) -> None:
#     concept_uris_batch: list[URIRef] = []
#     with ReleaseGraph.open(input_, read_only=True) as release_graph:
#         for concept_uri in release_graph.concept_uris:
#             concept_uris_batch.append(concept_uri)
#             if len(concept_uris_batch) == _CONCEPT_BATCH_SIZE:
#                 work_queue.put(tuple(concept_uris_batch))
#                 concept_uris_batch = []
#
#     if concept_uris_batch:
#         work_queue.put(tuple(concept_uris_batch))


def transform_release_graph_to_interchange_models(
    release_graph_descriptor: ReleaseGraph.Descriptor,
) -> Iterable[interchange.Model]:
    with ReleaseGraph.open(release_graph_descriptor, read_only=True) as release_graph:
        concept_scheme = release_graph.concept_scheme
        yield interchange.Node.builder(uri=concept_scheme.uri).add_rdf_type(
            SKOS.ConceptScheme
        ).set_modified(concept_scheme.modified).build()
        yield from __transform_labels(concept_scheme)

        for concept in release_graph.concepts:
            yield from __transform_concept(
                concept=concept, concept_scheme_uri=concept_scheme.uri
            )

    # yield from parallel_transform(
    #     consumer=_transform_concept_consumer,
    #     consumer_input=(concept_scheme.uri, release_graph_descriptor),
    #     producer=_transform_concept_producer,
    #     producer_input=release_graph_descriptor,
    # )
