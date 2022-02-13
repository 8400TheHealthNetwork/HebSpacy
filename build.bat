python setup.py develop
python create_pipeline.py
python -m spacy package ./pipeline ./ --build wheel
python setup.py bdist_wheel