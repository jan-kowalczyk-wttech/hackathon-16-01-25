import os

import aws_cdk as cdk

from backend.backend_stack import BackendStack
from backend.s3_bucket import S3BucketStack


def get_env(app: cdk.App):
    env: str = os.environ.get("USER")
    if not env:
        raise Exception("ENV is not defined")

    print(f"Starting cdk on env ${env}")
    return env.replace(".","")


app = cdk.App()
env = get_env(app)


s3_stack = S3BucketStack(app, f"{env}S3BucketStack")
stack = BackendStack(app, f"{env}BackendStack")

s3_stack.upload_bucket.grant_read_write(stack.get_presigned_url_lambda)


app.synth()
