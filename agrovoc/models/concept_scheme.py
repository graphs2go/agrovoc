from graphs2go.models import skos

from agrovoc.models.label import Label


class ConceptScheme(skos.ConceptScheme):
    _LABEL_CLASS = Label
