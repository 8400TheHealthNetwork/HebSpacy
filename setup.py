import os
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
parent_directory = os.path.abspath(os.path.join(this_directory, os.pardir))

VERSION = {}
with open(f"{this_directory}/hebspacy/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

def get_requirements_from_files(*files):
    install_requires = {}
    for filename in files:
        if os.path.isfile(filename):
            with open(filename) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "#" in line:
                            req, version = line.split("#")[0].strip().split("==")
                        else:
                            req, version = line, None

                        # requirement versions must be specified with "==", otherwise the line above will fail
                        if req not in install_requires:
                            install_requires[req] = version
    reqs = []
    for k, v in sorted(install_requires.items()):
        if v:
            reqs.append(f"{k}=={v}")
        else:
            reqs.append(k)
    return reqs


install_requires_ = get_requirements_from_files('requirements.txt')

for requirement in install_requires_:
    print("adding requirement: " + requirement)

with open(path.join(parent_directory, "README.MD"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hebspacy",
    author="hebpsacy",
    version=VERSION["VERSION"],
    author_email="hebspacy@gmail.com",
    url="https://github.com/8400TheHealthNetwork/HebSpacy",
    license="MIT License (MIT)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="SpaCy pipeline and models for Hebrew text",
    keywords=["hebrew nlp spacy SpaCy phi pii"],
    entry_points={
        "spacy_factories": ["ner_head = hebspacy.ner_head:NERHead",
                            "consolidator = hebspacy.ner_head:consolidator"]
    },
    packages=find_packages(),
    install_requires=install_requires_,
    python_requires=">=3.8.0",
)
