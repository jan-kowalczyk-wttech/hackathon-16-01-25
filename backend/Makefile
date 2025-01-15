

install:
	# To install poetry dependencies and lambda dependencies
	poetry install && ./lambda_dep_init.sh
deploy:
	cdk deploy
watch:
	# To use live reload
	cdk watch