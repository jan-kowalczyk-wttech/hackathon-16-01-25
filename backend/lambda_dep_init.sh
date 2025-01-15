poetry export --without-hashes -f requirements.txt -o requirements.txt

mkdir -d lambda/dependencies/python
poetry run pip install -r requirements.txt -t lambda/dependencies/python --upgrade