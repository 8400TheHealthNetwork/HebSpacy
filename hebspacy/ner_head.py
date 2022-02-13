import inspect
import json
from collections import defaultdict

import numpy as np
import torch
from spacy import Language
from spacy.tokens import Doc, Span
from spacy.training import iob_to_biluo, biluo_tags_to_spans
from torch.nn import functional as funct


@Language.factory("ner_head")
class NERHead:
    def __init__(self, nlp: Language, name: str):
        self.name = name
        Doc.set_extension(f"{name}_ents", default=None, force=True)
        Span.set_extension("confidence_score", default=1.0, force=True)


    def load(self, dir_path: str):
        self.model = torch.load(f"{dir_path}/{self.name}.bin")
        with open(f"{dir_path}/{self.name}.json", "r") as f:
            self.idx_to_tag = json.load(f)

    def __call__(self, doc):
        tokens_pred = []
        probs_pred = []
        # sequence length is defined by the longest sentence (shorter sentences are padded sentences)
        seq_size = len(doc._.trf_data.wordpieces.strings[-1])

        for index, token in enumerate(doc):
            # check if a word piece exist for the token
            if len(doc._.trf_data.align[index].dataXd) > 0:
                # retrieve the index of the token head word piece
                wp_index = doc._.trf_data.align[index].dataXd[0][0]
                # calculate the location of the vector when considering the batches
                batch = wp_index // seq_size
                item = wp_index % seq_size

                # retrieving the vectors of the token's head word piece from the last 4 layers
                layer_9 = torch.from_numpy(doc._.trf_data.tensors[2][8][batch][item])
                layer_10 = torch.from_numpy(doc._.trf_data.tensors[2][9][batch][item])
                layer_11 = torch.from_numpy(doc._.trf_data.tensors[2][10][batch][item])
                layer_12 = torch.from_numpy(doc._.trf_data.tensors[2][11][batch][item])

                # concat the vectors into one
                concatenated_vector = torch.cat([layer_9, layer_10, layer_11, layer_12])

                # calculate the logits
                logits = funct.linear(concatenated_vector, self.model["weight"], self.model["bias"])

                pred = torch.argmax(logits).numpy().tolist()

                # calculate probabilities and save the score for the top class
                prob = torch.softmax(torch.FloatTensor(logits), dim=-1)
                probs_pred.append(prob[pred].tolist())

                if pred == 0:
                    pred = 1
            else:
                pred = 1
                probs_pred.append(1)
            tokens_pred.append(self.idx_to_tag[str(pred)])
        biluo_tags = iob_to_biluo(tokens_pred)
        spans = biluo_tags_to_spans(doc, biluo_tags)

        # entity confidence score is the average score across the corresponding tokens
        for span in spans:
            span._.confidence_score = np.average(probs_pred[span.start:span.end])
        doc = self.set_entities(doc, spans)

        return doc

    def to_disk(self, path, exclude=tuple()):
        # This will receive the directory path + /my_component
        model_path = path / "model.bin"
        torch.save(self.model, model_path)
        idx_to_tag_mapping_path = path / "idx_to_tag.json"
        with idx_to_tag_mapping_path.open("w", encoding="utf8") as f:
            f.write(json.dumps(self.idx_to_tag))

    def from_disk(self, path, exclude=tuple()):
        # This will receive the directory path + /my_component
        model_path = path / "model.bin"
        self.model = torch.load(model_path)
        idx_to_tag_mapping_path = path / "idx_to_tag.json"
        with idx_to_tag_mapping_path.open("r", encoding="utf8") as f:
            self.idx_to_tag = json.load(f)
        return self

    def set_entities(self, doc, spans):
        setattr(doc._, f"{self.name}_ents", spans)
        return doc


@Language.component("consolidator")
def consolidator(doc):
    """
    Weights the recognized entities from the different ner heads and selects a subset that do not non-overlap
    The current consolidation policy prefers entities first by starting position and then by length
    """

    # extract all all ner_head extensions
    extensions = filter(lambda ext: ext[0].endswith("_ents"), inspect.getmembers(doc._))
    ents = []
    start_to_entities = defaultdict(list)

    # map start index to entities
    for name, entities in extensions:
        for entity in entities:
            start_to_entities[entity.start].append(entity)

    # iterate over the starting position and select the longest entity
    start_positions = sorted(list(start_to_entities.keys()))
    max_index = start_positions[-1]
    index = 0
    while start_positions[index] <= max_index:
        start_index = start_positions[index]
        entities = start_to_entities[start_index]

        # find the longest entity
        ent_lens = list(map(lambda ent: len(ent), entities))
        max_value = max(ent_lens)
        arg_max = ent_lens.index(max_value)

        # select that entity
        target_entity = entities[arg_max]
        ents.append(target_entity)

        # find the next index to investigate
        min_target_index = start_index + len(target_entity)
        if max_index < min_target_index:
            break
        while start_positions[index] < min_target_index:
            index += 1

    doc.set_ents(ents)
    return doc

