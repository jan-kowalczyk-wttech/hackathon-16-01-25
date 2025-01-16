
install:
	# To install poetry dependencies and lambda dependencies
	poetry install && ./lambda_dep_init.sh
dev:
	NODE_OPTIONS=--max_old_space_size=60000 ENV=${USER} cdk deploy --all
dev-watch:
    NODE_OPTIONS=--max_old_space_size=60000 ENV=${USER} cdk watch