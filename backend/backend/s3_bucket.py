from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk.aws_s3 import Bucket, BucketAccessControl
from constructs import Construct


class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.upload_bucket = Bucket(
            self,
            "UploadBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            access_control=BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )