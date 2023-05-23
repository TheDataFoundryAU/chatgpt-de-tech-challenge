#!/usr/bin/env python3

import aws_cdk as cdk

from ingestion_lambda.ingestion_lambda_stack import IngestionLambdaStack

app = cdk.App()
IngestionLambdaStack(app, "ingestion-lambda")

app.synth()
