# Contribute your own `hebspacy` model
Your are welcome to contribute by training and packaging your own `hebspacy` model. Please follow the instructions below to enable seamless loading process

## Model Training
You may choose the training codebase that best fits your requirements as long as you save the following files:
1. The pretrained transformer layers (post-fine tuning) **separately** from the NER heads. file should be named `pytorch_model.bin`
2. All the files required to be loaded by `transformers.AutoModel`, including the standard `config.json`, `special_tokens.json`, `tokenizer_config.json`, `vocab.txt`.
3. Each of the NER head weights should be saved as separate `bin` file with a corresponding index to class mapping `json` file (see instructions below). Files should follow the `ner_<name>.bin` and `ner_<name>.json` name convention.

**All weights files should be trained using Hugging Face and PyTorch libraries**

For example, the following directory contains all the required files for a model that was jointly trained against the BMC and NEMO corpora:
````
resources/
├── config.json
├── pytorch_model.bin
├── special_tokens.json
├── tokenizer_config.json
├── vocab.txt
├── ner_bmc.bin
├── ner_bmc.json
├── ner_nemo.bin
└── ner_nemo.json
````

### Index to class mapping file
Each NER head should include a `json` file that maps between the model class index to the corresponding token class name.
Note that indices `0` and `1` should always be associated with `[PAD]` and `O` classes, respectively. Also, the token annotation schema should be [**IBO2**](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)).


Here is an example of the index to class mapping `json` file for `ner_bmc`:
````json
{
	"0": "[PAD]",
	"1": "O",
	"2": "B-PERS",
	"3": "I-PERS",
	"4": "B-LOC",
	"5": "I-LOC",
	"6": "B-ORG",
	"7": "I-ORG",
	"8": "B-TIME",
	"9": "I-TIME",
	"10": "B-DATE",
	"11": "I-DATE",
	"12": "B-MONEY",
	"13": "I-MONEY",
	"14": "B-PERCENT",
	"15": "I-PERCENT",
	"16": "B-MISC__AFF",
	"17": "I-MISC__AFF",
	"18": "B-MISC__ENT",
	"19": "I-MISC__ENT",
	"20": "B-MISC_EVENT",
	"21": "I-MISC_EVENT"
}
````

## Model Packaging
Once you have prepared all the directory with all required files, please follow these steps:
1. Fork this repo (in case you haven't already)
2. Make sure that `spacy` is installed in your running python environment (**make sure it is the same version as mentioned in requirements.txt**) 
3. Navigate to the repo's root
4. Run `python setup.py develop`, which should create a `hebspacy.egg-info` directory
5. Navigate to `scripts\model`
6. Update `meta.json` accordingly (make sure to follow the [spaCy package naming conventions](https://spacy.io/models#conventions))
7. Run `python package.py <RESOURCES_DIR> <OUTPUT_DIR>`, where `<RESOURCES_DIR>` should point to the directory with all the files from the previous section.
8. Run `python -m spacy package <OUTPUT_DIR> <WHEEL_DIR> --build wheel`
9. Your `whl` and `tar.gz` files are ready under `<WHEEL_DIR>/<lang>_<name>-<version>/dist`
10. Install your files by running `pip install XXXXX.whl`