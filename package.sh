#!/bin/bash

mkdir -p dist.bkp
cp -a dist/. dist.bkp/
rm -R dist/*

python3 -m build
python3 -m twine upload dist/* --repository testpypi --config-file ~/.pypirc 

echo "Download upgrade (may take time to be available):"
echo "pip install -i https://test.pypi.org/simple/ -U ansible-butler==0.0.<x>"