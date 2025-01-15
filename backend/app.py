import aws_cdk as cdk

from backend.backend_stack import BackendStack
from backend.s3_bucket import S3BucketStack

env = cdk.Environment(account="833887979428", region="us-west-2")


app = cdk.App()
s3_stack = S3BucketStack(app, "S3BucketStack", env=env)
stack = BackendStack(app, "BackendStack", env=env)

s3_stack.upload_bucket.grant_read_write(stack.get_presigned_url_lambda)


app.synth()
