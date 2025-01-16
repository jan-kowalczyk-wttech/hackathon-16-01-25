
install:
	# To install poetry dependencies and lambda dependencies
	poetry install && ./lambda_dep_init.sh
dev:
	 NODE_OPTIONS=--max_old_space_size=6000 ENV=${USER} cdk deploy --all
dev-watch:
	# To use live reload
    NODE_OPTIONS=--max_old_space_size=6000 ENV=${USER} cdk watch