# Weather Data Ingestion Service

This service uses AWS Lambda and the Open-Meteo API to fetch and store weather data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of AWS CLI.
* You have installed the AWS CDK.
* You have installed Docker.
* You have installed Python 3.8 or later.
* You have a suitable AWS account.
* You have set up your AWS credentials using `aws configure`.

## Deploying the Stack

1. Initialize a new CDK project (if you haven't already):

```bash
cdk init app --language=python
```

2. Install necessary CDK libraries:

```bash
pip install aws-cdk.aws-s3 aws-cdk.aws-lambda aws-cdk.aws-events aws-cdk.aws-events-targets aws-cdk.aws-iam
```

3. Copy the Python files from this repository into the `lambda` directory of your CDK project.

4. Run the following command to deploy the CDK stack:

```bash
cdk deploy
```

## Installing Dependencies

In the `lambda` folder, run the following command to generate a `dependencies.zip` file that includes the necessary Python libraries for the Lambda function:

```bash
chmod +x build-dependancies.sh
./build-dependancies.sh
```

## Using Weather Data Ingestion Service

The service will automatically fetch weather data every 5 minutes and store the data in an S3 bucket.

## Contact

If you want to contact me you can reach me at `<your-email>`.

---

Please adapt the README to your specific project, needs, and environment.