import aws_cdk.aws_lambda as _lambda
from constructs import Construct

class OurFunction(_lambda.Function):
    def __init__(self, scope: Construct, construct_id: str, dependency_layer: _lambda.LayerVersion, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.add_layers(dependency_layer)