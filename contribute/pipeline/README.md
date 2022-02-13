# Contribute to `hebspacy` pipeline
In case you added new feature, fixed bugs or made any changes in the repo, please follow these instructions:

1. Run existing and new tests on your code. make sure to place them under `/tests`
2. Navigate to `hebspacy/version.py` and promote the package version according to [semantic versioning scheme](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred)
3. Run `python setup.py bdist_wheel` to create a new `whl` file
4. You can now install your version by running `pip install XXXXX.whl`
5. Once you are ready to upload your version to [PyPi](https://pypi.org/project/hebspacy/), please contact the package maintainers personally or via email to [hebspacy@gmail.com](mailto:hebspacy@gmail.com)

Note that previous model files may need to be repackaged to work with the new version. 