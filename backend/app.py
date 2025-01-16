import os

import aws_cdk as cdk

from backend.backend_stack import BackendStack

def get_env(app: cdk.App):
    env: str = os.environ.get("USER")
    if not env:
        raise Exception("ENV is not defined")
    env =  env.replace(".","")
    print(f"Starting cdk on env {env}")
    return env


app = cdk.App()
env = get_env(app)

region = cdk.Environment(account="833887979428", region="us-west-2")
stack = BackendStack(app, f"{env}BackendStack", env=region)

app.synth()
