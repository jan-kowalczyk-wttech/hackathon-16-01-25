poetry export --without-hashes -f requirements.txt -o requirements.txt
rm -rf lambda/dependencies
mkdir lambda/dependencies
mkdir lambda/dependencies/python
poetry run pip install --platform manylinux2014_x86_64 --python-version 3.12 --only-binary:all: -r requirements.txt -t lambda/dependencies/python --upgrade