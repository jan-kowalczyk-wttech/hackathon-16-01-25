poetry export --without-hashes -f requirements.txt -o requirements.txt

mkdir -d lambda_dependencies/python
poetry run pip install -r requirements.txt -t lambda_dependencies/python --upgrade