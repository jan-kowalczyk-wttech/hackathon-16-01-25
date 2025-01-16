from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk.aws_s3 import Bucket, BucketAccessControl
from constructs import Construct


class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
