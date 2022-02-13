# HebSpaCy

This repository contains custom spaCy pipes and models for Hebrew text.

In particular, the pipeline includes a dedicated Hebrew based NER model. 
The model uses [AlephBert](https://arxiv.org/pdf/2104.04052.pdf) as its pretrained model 
coupled with two NER focused heads - forming a transformer based multitask NER model. The model is trained on two publicly available NER-annotated Hebrew corpora:
1. [NEMO corpus](https://github.com/OnlpLab/NEMO-Corpus) - annotations of the Hebrew Treebank (Haaretz newspaper) for the widely-used OntoNotes entity category: `GPE` (geo-political entity), `PER` (person), `LOC` (location), `ORG` (organization), `FAC` (facility), `EVE` (event), `WOA` (work-of-art), `ANG` (language), `DUC` (product). 
2. [BMC](https://www.cs.bgu.ac.il/~elhadad/nlpproj/naama/) - annotations of articles from Israeli newspapers and websites (Haaretz newspaper, Maariv newspaper, Channel 7) for the common entity categories: `PERS` (person), `LOC` (location), `ORG` (organization), `DATE` (date), `TIME` (time), `MONEY` (money), `PERCENT` (percent), `MISC__AFF` (misc affiliation), `MISC__ENT` (misc entity),
 `MISC_EVENT` (misc event).

The Hugging Face library and PyTorch were used to build the model. 

### Model integration
We separated the output multitask model into three separate weight files: the transfomer embeddings, the BMC head, and the NEMO head.
Each component was wrapped in a separate pipe and integrated into the custom pipeline. 
Additionally, a custom head consolidation pipe was added after the model pipes to address overlaps and conflicts.
Nevertheless, the recognized entities by each head can be accessed in the spacy `Doc` through the dedicated attribute extensions (i.e., `doc._.nemo_ents` and `doc._.bmc_ents)`.


## Installation
1. Installing the `hebspacy` library and installing the model:
```bash
pip install hebspacy
```

2. Downloading the model `.whl` file from [here](https://1drv.ms/u/s!AroScutHvkt-acIaYYFflQHwUrA?e=n6EvV0)

3. Install a model:
```bash
pip install </path/to/download>
```

Note: We strongly recommend that you use an isolated Python environment to install hebspacy.
Additionally, hebspacy works best for **Python 3.8 or greater**.


#### Setting up a virtual environment

[Conda](https://conda.io/) can be used set up a virtual environment with the
version of Python required for hebspacy.  If you already have a Python 3.8
environment you want to use, you can skip to the 'installing via pip' section.

1.  [Follow the installation instructions for Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html?highlight=conda#regular-installation).

2.  Create a Conda environment called `hebspacy` with Python 3.8:

    ```bash
    conda create -n hebspacy python=3.8
    ```

3.  Activate the Conda environment. You will need to activate the Conda environment in each terminal in which you want to use hebspacy.

    ```bash
    source activate hebspacy
    ```

Now you can install `hebspacy` and the model using the steps above.


Once you have completed the above steps and downloaded one of the models below, you can load a hebspacy model as you would any other spaCy model. For example:
```python
import spacy
nlp = spacy.load("he_ner_news_trf")
doc = nlp("גדעון לבנה הגיע היום לבית החולים שערי צדק עם תלונות על כאבים בחזה")
```

#### Note on upgrading
If you are upgrading `hebspacy`, you will need to download the models again, to get the model versions compatible with the version of `hebspacy` that you have. The link to the model that you download should contain the version number of `hebspacy` that you have.

#### Example Usage
```python
import spacy

nlp = spacy.load("he_ner_news_trf")
text = """מרגלית דהן
מספר זהות 11278904-5

2/12/2001
ביקור חוזר מ18.11.2001
במסגרת בירור פלפיטציות ואי סבילות למאמצים,מנורגיות קשות ע"ר שרירנים- ביצעה מעבדה שהדגימה:
המוגלובין 9, מיקרוציטי היפוכרומטי עם RDW 19,
פריטין 10, סטורציית טרנספרין 8%. 
מבחינת עומס נגיפי HIV- undetectable ומקפידה על HAART
"""

doc = nlp(text)
for entity in doc.ents:
    print(f"{entity.text} \t {entity.label_} ({entity.start_char},{entity.end_char})")

>>> מרגלית דהן  PERS (0,10)
>>> 2/12/2001   DATE (33,42)
>>> מ18.11.2001 DATE (54,65)
>>> 8%  PERCENT (230,232)

```

## Model Customization
TODO 

-----

HebSpaCy is an open-source project developed by [8400 The Health Network](https://www.8400thn.org/).