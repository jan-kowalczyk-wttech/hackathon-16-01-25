from aws_cdk import (
    Stack, aws_lambda as _lambda, Duration, aws_apigateway, RemovalPolicy
)
from aws_cdk.aws_apigateway import LambdaIntegration
from aws_cdk.aws_s3 import Bucket, BucketAccessControl
from constructs import Construct

from backend.util.our_function import OurFunction

LAMBDA_DEP = "lambda/dependencies"
LAMBDA_SRC = "lambda/src"

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.upload_bucket = self.create_upload_bucket()

        dependency_layer = self.create_lambda_dependency_layer()

        self.get_presigned_url_lambda = OurFunction(
            self,
            "GetPresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_presigned_url"),
            handler="get_presigned_url.lambda_handler",
            timeout=Duration.minutes(1),
            dependency_layer=dependency_layer,
            environment={
                'BUCKET_NAME': self.upload_bucket.bucket_name
            }
        )

        self.upload_bucket.grant_read_write(self.get_presigned_url_lambda)

        self.api = aws_apigateway.RestApi(self,f"{self.stack_name}BackendApi", deploy=True)

        self.add_api_resource("get-presigned-url","GET",self.get_presigned_url_lambda)

    def create_lambda_dependency_layer(self):
        return _lambda.LayerVersion(
            self,
            "DependencyLayer",
            code=_lambda.Code.from_asset(LAMBDA_DEP),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer with shared dependencies between lambdas",
        )

    def create_upload_bucket(self):
        return Bucket(
            self,
            "UploadBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            access_control=BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )

    def add_api_resource(self, path: str, method: str, handler: OurFunction):
        self.api.root.add_resource(path).add_method(method, LambdaIntegration(handler))
