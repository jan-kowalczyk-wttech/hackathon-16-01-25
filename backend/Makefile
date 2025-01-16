
install:
	# To install poetry dependencies and lambda dependencies
	poetry install && ./lambda_dep_init.sh

watch:
	NODE_OPTIONS=--max_old_space_size=60000 ENV=${USER} cdk watch

dev:
	NODE_OPTIONS=--max_old_space_size=60000 ENV=${USER} cdk deploy --all
