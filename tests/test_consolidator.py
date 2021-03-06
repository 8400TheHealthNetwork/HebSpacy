import pytest

from hebspacy.ner_head import NERHead, consolidator
from spacy.tokens import Doc, Span


def test_consolidator_with_single_head(he_vocab):
    """
    Checks that ner head entities are populated to ents property post consolidation
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    new_head = NERHead(nlp=None, name="test")
    entities = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 1, 2, label="LOC")]
    new_head.set_entities(mock_doc, entities)
    doc = consolidator(mock_doc)

    assert doc == mock_doc
    assert len(doc.ents) == 2
    assert doc.ents[0] == entities[0]
    assert doc.ents[1] == entities[1]


def test_consolidator_with_multiple_heads_ent_contained_in_ent(he_vocab):
    """
    Checks that in case of entity conflict, the consolidator prefers the longer term (assuming they share the same index)
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])

    new_head = NERHead(nlp=None, name="test")
    entities_test = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 1, 2, label="LOC")]
    new_head.set_entities(mock_doc, entities_test)

    new_head = NERHead(nlp=None, name="test_2")
    entities_test_2 = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 1, 3, label="LOC")]
    new_head.set_entities(mock_doc, entities_test_2)

    doc = consolidator(mock_doc)

    assert doc == mock_doc
    assert len(doc.ents) == 2
    assert doc.ents[0].start == entities_test[0].start and doc.ents[0].end == entities_test[0].end
    assert doc.ents[1].start == entities_test_2[1].start and doc.ents[1].end == entities_test_2[1].end


def test_consolidator_with_multiple_heads_ents_conflicts(he_vocab):
    """
    Checks that in case of entity conflict/paritial overlap, the consolidator prefers position
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף", "8"])

    new_head = NERHead(nlp=None, name="test")
    entities_test = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 1, 3, label="LOC")]
    new_head.set_entities(mock_doc, entities_test)

    new_head = NERHead(nlp=None, name="test_2")
    entities_test_2 = [Span(mock_doc, 0, 1, label="PERSON"), Span(mock_doc, 2, 4, label="LOC")]
    new_head.set_entities(mock_doc, entities_test_2)

    doc = consolidator(mock_doc)

    assert doc == mock_doc
    assert len(doc.ents) == 2
    assert doc.ents[0].start == entities_test[0].start and doc.ents[0].end == entities_test[0].end
    assert doc.ents[1].start == entities_test[1].start and doc.ents[1].end == entities_test[1].end


def test_consolidator_with_no_heads(he_vocab):
    """
    make sure consolidator doesn't crash in case there are no ner heads
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    try:
        doc = consolidator(mock_doc)
    except Exception as e:
        pytest.fail("Unexpected error", str(e))


def test_consolidator_with_head_not_initialized(he_vocab):
    """
    make sure consolidator doesn't crash in case ner heads weren't initialized
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    new_head = NERHead(nlp=None, name="test")
    try:
        doc = consolidator(mock_doc)
    except IndexError as e:
        pytest.fail("Unexpected Index error", str(e))


def test_consolidator_with_head_no_entities(he_vocab):
    """
    make sure consolidator doesn't crash in case no entities were detected
    """
    mock_doc = Doc(he_vocab, words=["שלום", "כיתה", "אלף"])
    new_head = NERHead(nlp=None, name="test")
    new_head.set_entities(mock_doc, [])
    try:
        doc = consolidator(mock_doc)
    except IndexError as e:
        pytest.fail("Unexpected Index error", str(e))
