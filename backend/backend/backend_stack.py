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
        self.offer_creators_table = self.create_table_offer_creators()

        self.api = aws_apigateway.RestApi(self, f"{self.stack_name}BackendApi", deploy=True)
        self.presigned_url = self.get_presigned_url_lambda(dependency_layer)
        self.list_offers = self.get_list_offers_lambda()
        self.get_offer_by_id = self.get_offer_by_id_lambda()

        self.check_input = self.check_input_lambda()
        self.categorize_object = self.categorize_object_lambda()
        self.define_object = self.define_object_lambda()
        
        
        self.check_needed_information = self.check_needed_information_lambda()
        self.create_offer_creator_lambda = self.create_offer_creator_lambda()
        self.active_creator_lambda = self.get_active_creator_lambda()

    def check_input_lambda(self):
        check_input = Function(
            self,
            f"{self.stack_name}CheckInputLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/check_input"),
            handler="check_input.lambda_handler",
            timeout=Duration.minutes(1),
        )
        self.offers_table.grant_read_write_data(check_input)
        self.upload_bucket.grant_read_write(check_input)
        self.add_api_resource(["check-input"], "POST", check_input)
        return check_input

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

    def categorize_object_lambda(self):
        categorize_object = Function(
            self,
            f"{self.stack_name}CategorizeObjectLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/categorize_object"),
            handler="categorize_object.lambda_handler",
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
        self.offers_table.grant_read_write_data(categorize_object)
        self.upload_bucket.grant_read_write(categorize_object)
        self.add_api_resource(["categorize-object"], "POST", categorize_object)
        return categorize_object


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

    def create_offer_creator_lambda(self):
        create_offer_creator = Function(
            self,
            f"{self.stack_name}CreateOfferCreatorLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/create_offer_creator"),
            handler="create_offer_creator.lambda_handler",
            timeout=Duration.minutes(1),
            environment={
                'OFFER_CREATORS_TABLE': self.offer_creators_table.table_name
            }
        )
        self.offer_creators_table.grant_read_write_data(create_offer_creator)
        self.add_api_resource(["create-offer-creator"], "POST", create_offer_creator)
        return create_offer_creator
    
    def check_needed_information_lambda(self):
        check_needed_information = Function(
            self,
            f"{self.stack_name}CheckNeededInformationLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/check_needed_information"),
            handler="check_needed_information.lambda_handler",
            timeout=Duration.minutes(1),
            initial_policy=[
                PolicyStatement(
                    effect=Effect.ALLOW,
                    actions= ['bedrock:InvokeModel'],
                    resources=['*']
                )
            ],
            environment={
                'OFFER_CREATORS_TABLE': self.offer_creators_table.table_name
            }
        )
        self.offer_creators_table.grant_read_write_data(check_needed_information)
        self.add_api_resource(["check-needed-information"], "POST", check_needed_information)
        return check_needed_information

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

    def create_table_offer_creators(self):
        table = dynamodb.Table(
          self,
      f"{self.stack_name}OfferCreators",
          partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING),
          billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
          removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
        )

        table.add_global_secondary_index(
            index_name="UserIdIndex",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING)
        )

        return table

    def get_active_creator_lambda(self):
        get_active_creator = Function(
            self,
            f"{self.stack_name}GetActiveCreatorLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_active_creator"),
            handler="get_active_creator.lambda_handler",
            timeout=Duration.minutes(1),
            environment={
                'OFFER_CREATORS_TABLE': self.offer_creators_table.table_name
            }
        )
        self.offer_creators_table.grant_read_data(get_active_creator)
        self.add_api_resource(["get-active-creator", '{user_id}'], "GET", get_active_creator)
        return get_active_creator

    def add_api_resource(self, path: list[str], method: str, handler: Function):
        current_resource = self.api.root
        for p in path:
            current_resource = current_resource.add_resource(p)
        current_resource.add_method(method, LambdaIntegration(handler))
