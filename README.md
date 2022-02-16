# HebSpaCy 

A custom spaCy pipeline for Hebrew text including a transformer-based multitask NER model that recognizes 16 entity types in Hebrew, including `GPE`, `PER`, `LOC` and `ORG`.

----
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT) ![Release](https://img.shields.io/github/v/release/8400TheHealthNetwork/HebSpacy.svg) [![PyPI version](https://badge.fury.io/py/hebspacy.svg)](https://badge.fury.io/py/hebspacy) [![Pypi Downloads](https://img.shields.io/pypi/dm/hebspacy.svg)](https://img.shields.io/pypi/dm/hebspacy.svg) 

## Installation

To run the package you will need to install the package as well as the model, preferably in a virtual environment:

``` sh
# Create conda env (optional)
conda create --name hebspacy python=3.8
conda activate hebsafeharbor

# Install hebspacy
pip install hebspacy

# Download and install the model (see below availbable models)
pip install </path/to/download>
```

#### Available Models
| Model | Description | Install URL |
| ----- | ----------- | ----------- |
| he_ner_news_trf | A full spaCy pipeline for Hebrew text including a multitask NER model trained against the BMC and NEMO corpora. Read more [here](#he_ner_news_trf).| [Download](https://github.com/dkarmon/HebSpacy/releases/download/he_ner_news_trf-3.2.1/he_ner_news_trf-3.2.1-py3-none-any.whl)


## Getting started
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
    print(f"{entity.text} \t {entity.label_}: {entity._.confidence_score:.4f} ({entity.start_char},{entity.end_char})")

>>> מרגלית דהן	 PERS: 0.9999 (0,10)
>>> 2/12/2001 	 DATE: 0.9897 (33,42)
>>> מ18.11.2001 	 DATE: 0.8282 (54,65)
>>> 8% 	 PERCENT: 0.9932 (230,232)
```

---------------
### he_ner_news_trf
'he_ner_news_trf' is a multitask model constructed from [AlephBert](https://arxiv.org/pdf/2104.04052.pdf) and two NER focused heads, each trained against a different NER-annotated Hebrew corpus:
1. [NEMO corpus](https://github.com/OnlpLab/NEMO-Corpus) - annotations of the Hebrew Treebank (Haaretz newspaper) for the widely-used OntoNotes entity category: `GPE` (geo-political entity), `PER` (person), `LOC` (location), `ORG` (organization), `FAC` (facility), `EVE` (event), `WOA` (work-of-art), `ANG` (language), `DUC` (product). 
2. [BMC corpus](https://www.cs.bgu.ac.il/~elhadad/nlpproj/naama/) - annotations of articles from Israeli newspapers and websites (Haaretz newspaper, Maariv newspaper, Channel 7) for the common entity categories: `PERS` (person), `LOC` (location), `ORG` (organization), `DATE` (date), `TIME` (time), `MONEY` (money), `PERCENT` (percent), `MISC__AFF` (misc affiliation), `MISC__ENT` (misc entity),
 `MISC_EVENT` (misc event).

The model was developed and trained using the Hugging Face and PyTorch libraries, and was later integrated into a spaCy pipeline. 

#### Model integration
The output model was split into three weight files: _the transformer embeddings, the BMC head, and the NEMO head_.
The components were each packaged in a separate pipe and integrated into the custom pipeline. 
Furthermore, a custom NER head consolidation pipe was added last to address signal conflicts/overlaps, and sets the `Doc.ents` property.

To access the entities recognized by each NER head, use the `Doc._.<ner_head>` property (e.g., `doc._.nemo_ents` and `doc._.bmc_ents`).

--------------
## Contribution
You are welcome to contribute to `hebspacy` project and introduce new feature/ models. 
Kindly follow the [pipeline codebase instructions](contribute/pipeline/README.md) and the [model training and packaging guidelines](contribute/model/README.md).


-----

HebSpaCy is an open-source project developed by [8400 The Health Network](https://www.8400thn.org/).
