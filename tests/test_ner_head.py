import pytest
from hebspacy.ner_head import NERHead
from spacy.tokens import Doc, Span
from spacy.tokens.doc import Underscore


@pytest.fixture(autouse=True)
def remove_extensions():
    """
    Remove extensions as it is global
    """
    if Span.has_extension("confidence_score"):
        Span.remove_extension("confidence_score")

    # remove ner head entities extensions ({name}_ents)
    doc_extension_names = list(filter(lambda name: name.endswith("_ents"), Underscore.doc_extensions.keys()))
    for name in doc_extension_names:
        Underscore.doc_extensions.pop(name)

def test_span_confidence_score_extension_added(he_vocab):
    new_head = NERHead(nlp=None, name="test")
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    span = Span(mock_doc, 0, 1, label="PERSON")

    assert Span.has_extension("confidence_score")


def test_confidence_score(he_vocab):
    new_head = NERHead(nlp=None, name="test")
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    span = Span(mock_doc, 0, 1, label="PERSON")
    span._.confidence_score = 0.92

    new_head.set_entities(mock_doc, [span])

    assert mock_doc._.test_ents[0] == span
    assert mock_doc._.test_ents[0]._.confidence_score == span._.confidence_score


def test_create_new_head_and_set_entities(he_vocab):
    new_head = NERHead(nlp=None, name="test")
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    entities = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 1, 2, label="LOC")]
    new_head.set_entities(mock_doc, entities)

    assert Doc.has_extension("test_ents")
    assert mock_doc._.test_ents == entities
