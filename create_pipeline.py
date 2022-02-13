import json
import os
import shutil
from pathlib import Path
from spacy.lang.xx import MultiLanguage
from thinc.config import Config
import argparse

def create_pipeline():
    # before running the script run in terminal:
    # cd heb_spacy
    # python setup.py develop
    input_dir = Path(r"C:\Users\dakarmon\projects\HebSpacy\resources")
    target_dir = Path("pipeline")

    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir()

    nlp = MultiLanguage()
    # update metadata
    with open("meta.json", "r") as f:
        meta = json.load(f)
    nlp.meta.update(meta)

    # Add sentence segmentation
    nlp.add_pipe("sentencizer")

    # Add transformer
    config = Config().from_disk(input_dir / "transformer.cfg")
    transformer_config = config["transformer"]
    transformer_config["model"]["name"] = str(input_dir)
    transformer = nlp.add_pipe("transformer", config=config["transformer"])
    transformer.model.initialize()

    # Add BMC head
    bmc = nlp.add_pipe("ner_head", name="bmc", last=True)
    bmc.load(input_dir)
    os.mkdir(target_dir / "bmc")

    # Add NEMO head
    nemo = nlp.add_pipe("ner_head", name="nemo", last=True)
    nemo.load(input_dir)
    os.mkdir(target_dir / "nemo")

    # Add consolidator
    nlp.add_pipe("consolidator", last=True)

    nlp.to_disk(target_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('resources_dir', type=str, required=True, dest="path to the directory containing the weights and configuration files")
    args = parser.parse_args()

    create_pipeline()
