#!/usr/bin/env python3

from aws_cdk import core

from ingestion_lambda.ingestion_lambda_stack import IngestionLambdaStack

app = core.App()
IngestionLambdaStack(app, "ingestion-lambda")

app.synth()
