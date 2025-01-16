
install:
	# To install poetry dependencies and lambda dependencies
	poetry install && ./lambda_dep_init.sh
dev:
	ENV=${USER} cdk deploy --all
dev-watch:
	# To use live reload
	ENV=${USER} cdk watch