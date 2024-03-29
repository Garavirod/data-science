from aws_cdk import (
    Stack,
    aws_s3 as S3,
    aws_lambda as Lambda,
    Size,
    Duration,
    aws_events as events,
    aws_events_targets as targets
)
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()


class AwsStackStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        buckets = {
            'input_bucket': S3.Bucket(
                self,
                'input-data-youtube-channel',
                bucket_name='input-data-youtube-channel',
                versioned=True
            ),
            'output_bucket': S3.Bucket(
                self,
                'output-data-youtube-channel',
                versioned=True,
                bucket_name='output-data-youtube-channel',
            ),

        }

        event_bridge_schedules = {
            'youtube-analytics_cron':events.Rule(
                self,
                "Run Daily at 12:30 hrs UTC",
                rule_name="youtube-analytics_cron",
                schedule=events.Schedule.cron(
                    hour='12',
                    minute='30',
                    week_day='*',
                    month='*',
                    year='*',
                )
            )
        }

        handlers = {
            'youtube_analytics_handler': Lambda.Function(
                self,
                'youtube-analytics-handlers',
                function_name='youtube-analytics-handlers',
                runtime=Lambda.Runtime.PYTHON_3_9,
                code=Lambda.Code.from_asset('handlers'),
                handler='youtube-analytics.handler',
                memory_size=512,
                ephemeral_storage_size=Size.mebibytes(512),
                timeout=Duration.minutes(2),  # 2 min,
                environment={
                    'BUCKET_INPUT_DATA': 'input-data-youtube-channel',
                    'BUCKET_OUTPUT_DATA': 'output-data-youtube-channel',
                    'YOUTUBE_API_KEY': os.getenv('API_YOUTUBE_KEY_DEV'),
                    'FILE_CHANNELS_DATA_SET': 'channels.csv'
                },
            ),
        }

        # Grants lambda permissions
        buckets['input_bucket'].grant_read(handlers['youtube_analytics_handler'])
        buckets['output_bucket'].grant_write(handlers['youtube_analytics_handler'])

        # Link event bridge to lambda handler
        event_bridge_schedules['youtube-analytics_cron'].add_target(
            targets.LambdaFunction(handler=handlers['youtube_analytics_handler'])
        )