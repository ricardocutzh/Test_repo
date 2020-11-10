import boto3
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        logger.info(">> context: {event}".format(event = str(event)))
        client = boto3.client('codepipeline')
        if update_source('v1.14.zip'):
            response = client.start_pipeline_execution('xcm-staging-codepipeline')
            logger.info(">> pipeline started")
        else:
            logger.info('>> pipeline not started')
    except Exception as e:
        logger.info('>> Lambda Handler Error: {Error} '.format(Error = str(e)))


def update_source(s3_file):
    try:
        client = boto3.client('codepipeline')
        response = client.update_pipeline(
            pipeline={
                'name': 'xcm-staging-codepipeline',
                'roleArn': 'arn:aws:iam::695292474035:role/ricardo-test-xclaim-CodePipelineServiceRole-ED87LFPZQOS5',
                'artifactStore': {
                    'type': 'S3',
                    'location': 'ricardo-nclouds-bucket'
                },
                'stages': [
                    {
                        'name': 'Source',
                        'actions': [
                            {
                                'name': 'App',
                                'actionTypeId': {
                                    'category': 'Source',
                                    'owner': 'AWS',
                                    'provider': 'S3',
                                    'version': '1'
                                },
                                'runOrder': 1,
                                'configuration': {
                                    'S3Bucket': 'ricardo-nclouds-bucket',
                                    'S3ObjectKey': s3_file,
                                    'PollForSourceChanges':'false'
                                },
                                'outputArtifacts': [
                                    {
                                        'name': 'App'
                                    },
                                ],
                                'roleArn': 'arn:aws:iam::695292474035:role/ricardo-lambda-role',
                                'region': 'us-east-1'
                            }
                        ]
                    },
                    {
                        'name': 'Build',
                        'actions': [
                            {
                                'name': 'Build',
                                'actionTypeId': {
                                    'category': 'Build',
                                    'owner': 'AWS',
                                    'provider': 'CodeBuild',
                                    'version': '1'
                                },
                                'runOrder': 1,
                                'configuration': {
                                    'ProjectName': 'ricardo-codebuild'
                                },
                                'inputArtifacts': [
                                    {
                                        'name': 'App'
                                    },
                                ],
                                'roleArn': 'arn:aws:iam::695292474035:role/ricardo-lambda-role',
                                'region': 'us-east-1'
                            }
                        ]
                    }
                ]
            }
        )
        return True
    except Exception as e:
        logger.info('>> error while updating the pipeline: {error}'.format(error = str(e)))
        return False