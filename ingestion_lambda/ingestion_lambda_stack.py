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

        lambda_layer = _lambda.LayerVersion(
            self, "LambdaLayer",
            code=_lambda.Code.from_asset('lambda/dependencies'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
            description="Layer for pandas and pyarrow libraries"
        )

        lambda_function = _lambda.Function(
            self, 'IngestionLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.lambda_handler',
            role=role,
            layers=[lambda_layer],
            environment={
                'BUCKET_NAME': bucket.bucket_name,
                'WEATHER_API_URL': 'https://api.open-meteo.com/v1/forecast',
                'LATITUDE': '<your-latitude>',
                'LONGITUDE': '<your-longitude>'
            }
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )
        rule.add_target(targets.LambdaFunction(lambda_function))

        bucket.grant_put(role)
