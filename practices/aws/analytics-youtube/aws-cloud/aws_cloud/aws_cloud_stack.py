from aws_cdk import (
    Stack,
    aws_s3 as S3,
    aws_lambda as Lambda
)

from constructs import Construct

class AwsCloudStack(Stack):

    def __init__(self, scope:Construct, id:str, **Kwargs)->None:
        super().__init__(scope=scope, id=id, **kwargs)

    youtube_analytics_handler = Lambda.Function(
        self,
        function_name='youtube-analytics-handlers',
        runtime= Lambda.Runtime.PYTHON_3_9,
        code=Lambda.Code.from_asset('handlers'),
        handler='youtube-analytics.handler'
    )