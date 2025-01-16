from aws_cdk.aws_lambda import Function


class OurFunction(Function):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, function_name=id,**kwargs)
