from aws_cdk import (
    Stack,
)
from constructs import Construct

from backend.our_function import OurFunction

LAMBDA_DEP = "lambda/dependencies"
LAMBDA_SRC = "lambda/src"

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.dependency_layer = _lambda.LayerVersion(
            self,
            "DependencyLayer",
            code=_lambda.Code.from_asset(LAMBDA_DEP),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer with shared dependencies between lambdas",
        )


        hello_lambda = OurFunction(
            self,
            "HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_DIR}/hello"),
            handler="hello.handler"
        )
