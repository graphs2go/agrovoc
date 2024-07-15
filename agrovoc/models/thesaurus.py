from collections.abc import Iterable

from graphs2go.models import rdf
from rdflib import RDF, SKOS, URIRef

from agrovoc.models.concept import Concept
from agrovoc.models.concept_scheme import ConceptScheme


class Thesaurus(rdf.Graph[rdf.Model]):
    def concept_by_iri(self, iri: URIRef) -> Concept:
        # For performance reasons, don't check if it's actually a Concept
        return Concept(rdf.NamedResource(graph=self.rdflib_graph, iri=iri))

    def concepts(self) -> Iterable[Concept]:
        for concept_iri in self.concept_iris():
            yield self.concept_by_iri(concept_iri)

    def concept_iris(self) -> Iterable[URIRef]:
        for concept_iri in self.rdflib_graph.subjects(
            predicate=RDF.type, object=SKOS.Concept, unique=True
        ):
            assert isinstance(concept_iri, URIRef)
            yield concept_iri

    @property
    def concept_scheme(self) -> ConceptScheme:
        for iri in self.rdflib_graph.subjects(
            predicate=RDF.type, object=SKOS.ConceptScheme
        ):
            if isinstance(iri, URIRef):
                return ConceptScheme(
                    rdf.NamedResource(graph=self.rdflib_graph, iri=iri)
                )
        raise ValueError("no skos:ConceptScheme found")
