import json
import os
import shutil
from pathlib import Path
from spacy.lang.xx import MultiLanguage
from thinc.config import Config
import argparse


def package(resource_dir: str, output_dir: str):
    input_dir = Path(resource_dir)
    target_dir = Path(output_dir)

    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir()

    nlp = MultiLanguage()
    # update metadata
    with open("meta.json", "r") as f:
        meta = json.load(f)
    nlp.meta.update(meta)
    nlp.lang = "he"

    # Add sentence segmentation
    nlp.add_pipe("sentencizer")

    # Add transformer
    config = Config().from_disk("transformer.cfg")
    transformer_config = config["transformer"]
    transformer_config["model"]["name"] = str(input_dir)
    transformer = nlp.add_pipe("transformer", config=config["transformer"])
    transformer.model.initialize()

    # Add ner heads
    for ner_head in input_dir.glob("ner_*.bin"):
        pipe = nlp.add_pipe("ner_head", name=ner_head.stem, last=True)
        pipe.load(input_dir)
        os.mkdir(target_dir / ner_head.stem)

    # Add consolidator
    nlp.add_pipe("consolidator", last=True)

    nlp.to_disk(target_dir)


if __name__ == '__main__':
    # make sure to run `python setup.py develop` before running this script
    parser = argparse.ArgumentParser()
    parser.add_argument('resources_dir', help="directory containing the weights and configuration files")
    parser.add_argument('output_dir', default=".", help="pipeline output directory")

    args = parser.parse_args()

    create_pipeline(args.resources_dir, args.output_dir)
