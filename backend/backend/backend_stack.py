from aws_cdk import (
    Stack,
)
from constructs import Construct

from backend.util.our_function import OurFunction

LAMBDA_DEP = "lambda/dependencies"
LAMBDA_SRC = "lambda/src"

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        dependency_layer = _lambda.LayerVersion(
            self,
            "DependencyLayer",
            code=_lambda.Code.from_asset(LAMBDA_DEP),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer with shared dependencies between lambdas",
        )

        self.get_presigned_url_lambda = OurFunction(
            self,
            "GetPresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_presigned_url"),
            handler="get_presigned_url.lambda_handler",
            timeout=Duration.minutes(1),
            dependency_layer=dependency_layer
        )


        self.api = aws_apigateway.LambdaRestApi(
            self,
            "GetPresignedUrlApi",
            handler=self.get_presigned_url_lambda,
            proxy=False
        )

        items = self.api.root.add_resource("items")
        items.add_method("GET")


# Curl to upload text.txt file to S3 bucket
# curl -X PUT -T text.txt "https://s3bucketstackuploadbucketd2c1da78r81cvprwbvek.s3.us-west-2.amazonaws.com/text.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential