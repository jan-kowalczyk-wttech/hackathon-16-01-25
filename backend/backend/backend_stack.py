import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import (
    Stack, aws_lambda as _lambda, Duration, aws_apigateway, RemovalPolicy, aws_bedrock
)
from aws_cdk.aws_apigateway import LambdaIntegration
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import LayerVersion, Function
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

        self.offers_table = self.create_table_offers()

        self.api = aws_apigateway.RestApi(self, f"{self.stack_name}BackendApi", deploy=True)

        self.presigned_url = self.get_presigned_url_lambda(dependency_layer)
        self.list_offers = self.get_list_offers_lambda()
        self.get_offer_by_id = self.get_offer_by_id_lambda()

        self.define_object = self.define_object_lambda()

    def get_presigned_url_lambda(self, dependency_layer: LayerVersion):
        presigned_url = OurFunction(
            self,
            f"{self.stack_name}GetPresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_presigned_url"),
            handler="get_presigned_url.lambda_handler",
            timeout=Duration.minutes(1),
            dependency_layer=dependency_layer,
            environment={
                'BUCKET_NAME': self.upload_bucket.bucket_name
            }
        )
        self.upload_bucket.grant_read_write(presigned_url)
        self.add_api_resource(["get-presigned-url"], "GET", presigned_url)
        return presigned_url

    def get_list_offers_lambda(self):
        list_offers = Function(
            self,
            f"{self.stack_name}ListOffersLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/list_offers"),
            handler="list_offers.lambda_handler",
            timeout=Duration.minutes(1),
            environment={
                'OFFERS_TABLE': self.offers_table.table_name
            }
        )
        self.offers_table.grant_read_data(list_offers)
        self.add_api_resource(["list-offers"], "GET", list_offers)
        return list_offers

    def get_offer_by_id_lambda(self):
        get_offer_by_id = Function(
            self,
            f"{self.stack_name}GetOfferByIdLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_offer_by_id"),
            handler="get_offer_by_id.lambda_handler",
            timeout=Duration.minutes(1),
            environment={
                'OFFERS_TABLE': self.offers_table.table_name
            }
        )
        self.offers_table.grant_read_data(get_offer_by_id)
        self.add_api_resource(["get_offer","{id}"], "GET", get_offer_by_id)

        return get_offer_by_id

    def define_object_lambda(self):
        define_object = Function(
            self,
            f"{self.stack_name}DefineObjectLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/define_object"),
            handler="define_object.lambda_handler",
            timeout=Duration.minutes(1),
            initial_policy=[
                PolicyStatement(
                    effect=Effect.ALLOW,
                    actions= ['bedrock:InvokeModel'],
                    resources=['*']
                )
            ],
            environment={
                'BUCKET_NAME': self.upload_bucket.bucket_name
            }
        )
        self.offers_table.grant_read_write_data(define_object)
        self.upload_bucket.grant_read_write(define_object)
        self.add_api_resource(["define-object"], "POST", define_object)
        return define_object

    def create_lambda_dependency_layer(self):
        return _lambda.LayerVersion(
            self,
            f"{self.stack_name}DependencyLayer",
            code=_lambda.Code.from_asset(LAMBDA_DEP),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer with shared dependencies between lambdas",
        )

    def create_upload_bucket(self):
        return Bucket(
            self,
            f"{self.stack_name}UploadBucket",
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            access_control=BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )

    def create_table_offers(self):
        return dynamodb.Table(
          self,
      f"{self.stack_name}Offers",
          partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING),
          billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
          removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
      )

    def add_api_resource(self, path: list[str], method: str, handler: Function):
        current_resource = self.api.root
        for p in path:
            current_resource = current_resource.add_resource(p)
        current_resource.add_method(method, LambdaIntegration(handler))
