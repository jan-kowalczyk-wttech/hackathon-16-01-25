from aws_cdk import (
    Stack,
)
from constructs import Construct
LAMBDA_DIR = "src/lambda"

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        _lambda.Function(
            self,
            "HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_DIR}/hello"),
            handler="hello.handler"
        )
