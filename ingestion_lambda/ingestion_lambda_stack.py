from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    Stack,
    Duration
)
from constructs import Construct


class IngestionLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, "IngestionBucket")

        role = iam.Role(
            self,
            "lambda-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')]
        )

        # Pyarrow lambda layer
        lambda_layer_pyarrow = _lambda.LayerVersion(
            self, "ExistingLambdaLayer",
            code=_lambda.Code.from_asset('layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
            description="Layer for existing libraries"
        )

        # New lambda layer for pandas
        lambda_layer_pandas = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "LambdaLayerPandas",
            "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python38:7"
        )

        lambda_function = _lambda.Function(
            self, 'IngestionLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.lambda_handler',
            role=role,
            layers=[lambda_layer_pandas, lambda_layer_pyarrow],
            environment={
                'BUCKET_NAME': bucket.bucket_name,
                'WEATHER_API_URL': 'https://api.open-meteo.com/v1/forecast',
                'LATITUDE': '-37.813629',
                'LONGITUDE': '144.963058'
            },
            memory_size=512  # Set the memory size to 512 MB
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )
        rule.add_target(targets.LambdaFunction(lambda_function))

        bucket.grant_put(role)
