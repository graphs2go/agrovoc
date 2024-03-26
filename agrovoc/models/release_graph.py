from collections.abc import Iterable

from rdflib import URIRef, RDF, SKOS

from agrovoc.models.concept import Concept
from agrovoc.models.concept_scheme import ConceptScheme
from graphs2go.models import rdf


class ReleaseGraph(rdf.Graph):
    def concept_by_uri(self, uri: URIRef) -> Concept:
        # For performance reasons, don't check if it's actually a Concept
        return Concept(resource=self.rdflib_graph.resource(uri))

    @property
    def concepts(self) -> Iterable[Concept]:
        for concept_uri in self.concept_uris:
            yield self.concept_by_uri(concept_uri)

    @property
    def concept_uris(self) -> Iterable[URIRef]:
        for concept_uri in self.rdflib_graph.subjects(
            predicate=RDF.type, object=SKOS.Concept, unique=True
        ):
            assert isinstance(concept_uri, URIRef)
            yield concept_uri

    @property
    def concept_scheme(self) -> ConceptScheme:
        for uri in self.rdflib_graph.subjects(
            predicate=RDF.type, object=SKOS.ConceptScheme
        ):
            return ConceptScheme(resource=self.rdflib_graph.resource(uri))
        raise ValueError("no skos:ConceptScheme found")
