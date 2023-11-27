import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cloud.aws_cloud_stack import AwsCloudStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cloud/aws_cloud_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCloudStack(app, "aws-cloud")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
