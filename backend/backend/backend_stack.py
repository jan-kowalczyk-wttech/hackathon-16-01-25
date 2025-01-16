import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import (
    Stack, aws_lambda as _lambda, Duration, aws_apigateway, RemovalPolicy, aws_bedrock
)
from aws_cdk.aws_apigateway import LambdaIntegration
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_s3 import Bucket, BucketAccessControl
from constructs import Construct

from backend.ourlambda import OurFunction

LAMBDA_DEP = "lambda/dependencies"
LAMBDA_SRC = "lambda/src"


class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.upload_bucket = self.create_upload_bucket()

        self.offers_table = self.create_table_offers()
        self.offer_creators_table = self.create_table_offer_creators()
        self.actions_table = self.create_table_actions()

        self.api = aws_apigateway.RestApi(self, f"{self.stack_name}BackendApi", deploy=True)
        self.presigned_url = self.get_presigned_url_lambda()
        self.list_offers = self.get_list_offers_lambda()
        self.get_offer_by_id = self.get_offer_by_id_lambda()

        self.categorize_object = self.categorize_object_lambda()
        self.define_object = self.define_object_lambda()
        
        self.check_needed_information = self.check_needed_information_lambda()
        self.create_offer_creator_lambda = self.create_offer_creator_lambda()
        self.active_creator_lambda = self.get_active_creator_lambda()
        self.get_price = self.get_price_lambda()

    # LAMBDAS
    def get_presigned_url_lambda(self):
        presigned_url = OurFunction(
            self,
            f"{self.stack_name}GetPresignedUrlLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_presigned_url"),
            handler="get_presigned_url.lambda_handler",
            timeout=Duration.minutes(1),
            environment={
                'BUCKET_NAME': self.upload_bucket.bucket_name
            }
        )
        # "{creator_id}"
        self.upload_bucket.grant_read_write(presigned_url)
        self.add_api_resource(["get-presigned-url","{user_id}","{creator_id}"], "GET", presigned_url)
        return presigned_url
    
    def get_list_offers_lambda(self):
        list_offers = OurFunction(
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
        get_offer_by_id = OurFunction(
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
        categorize_object = OurFunction(
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
                'BUCKET_NAME': self.upload_bucket.bucket_name,
                'ACTIONS_TABLE': self.actions_table.table_name
            }
        )
        self.offers_table.grant_read_write_data(categorize_object)
        self.upload_bucket.grant_read_write(categorize_object)
        self.actions_table.grant_read_write_data(categorize_object)
        self.add_api_resource(["categorize-object"], "POST", categorize_object)
        return categorize_object
    
    def define_object_lambda(self):
        define_object = OurFunction(
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
                'BUCKET_NAME': self.upload_bucket.bucket_name,
                'ACTIONS_TABLE': self.actions_table.table_name
            }
        )
        self.offers_table.grant_read_write_data(define_object)
        self.upload_bucket.grant_read_write(define_object)
        self.actions_table.grant_read_write_data(define_object)
        self.add_api_resource(["define-object"], "POST", define_object)
        return define_object
    
    def create_offer_creator_lambda(self):
        create_offer_creator = OurFunction(
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
        check_needed_information = OurFunction(
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
                'ACTIONS_TABLE': self.actions_table.table_name
            }
        )
        self.actions_table.grant_read_write_data(check_needed_information)
        self.add_api_resource(["check-needed-information"], "POST", check_needed_information)
        return check_needed_information
    
    def get_active_creator_lambda(self):
        get_active_creator = OurFunction(
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
    
    def get_price_lambda(self):
        get_price = OurFunction(
            self,
            f"{self.stack_name}GetPriceLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset(f"{LAMBDA_SRC}/get_price"),
            handler="get_price.lambda_handler",
            timeout=Duration.minutes(1),
            initial_policy=[
                PolicyStatement(
                    effect=Effect.ALLOW,
                    actions= ['bedrock:InvokeModel'],
                    resources=['*']
                )
            ]
        )
        self.add_api_resource(["get_price"], "POST", get_price)
        return get_price

    # TABLES
    def create_table_offers(self):
        return dynamodb.Table(
          self,
          f"{self.stack_name}Offers",
          table_name= f"{self.stack_name}Offers",
          partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING),
          billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
          removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
        )
    def create_table_offer_creators(self):
        table = dynamodb.Table(
          self,
       f"{self.stack_name}OfferCreators",
          table_name= f"{self.stack_name}OfferCreators",
          partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING),
          billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
          removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
        )

        return table
    def create_table_actions(self):
        return dynamodb.Table(
          self,
      f"{self.stack_name}Actions",
          table_name= f"{self.stack_name}Actions",
          partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING),
          billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
          removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE
      )

    # BUCKET
    def create_upload_bucket(self):
        return Bucket(
            self,
            f"{self.stack_name}UploadBucket",
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            access_control=BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )

    # API GATEWAY
    def add_api_resource(self, path: list[str], method: str, handler: OurFunction):
        current_resource = self.api.root
        for p in path:
            current_resource = current_resource.add_resource(p)
        current_resource.add_method(method, LambdaIntegration(handler))
