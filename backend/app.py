import aws_cdk as cdk

from backend.backend_stack import BackendStack

env = cdk.Environment(account="833887979428", region="us-west-2")


app = cdk.App()
stack = BackendStack(app, "BackendStack", env=env)



app.synth()
