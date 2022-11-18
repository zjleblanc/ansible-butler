#!/bin/bash

mkdir -p dist.bkp
cp -a dist/. dist.bkp/
rm -R dist/*

python3 -m build
python3 -m twine upload dist/* --repository pypi --config ~/.pypirc