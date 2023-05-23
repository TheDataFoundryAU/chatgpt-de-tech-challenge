import aws_cdk as core
import aws_cdk.assertions as assertions

from 2023_05_23_test_gpt_repo.2023_05_23_test_gpt_repo_stack import 20230523TestGptRepoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 2023_05_23_test_gpt_repo/2023_05_23_test_gpt_repo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 20230523TestGptRepoStack(app, "2023-05-23-test-gpt-repo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
