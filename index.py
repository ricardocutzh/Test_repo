import boto3
import logging
import os
import time
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

S3BUCKET = os.environ['S3BUCKET']
BUILD_PACKAGE = os.environ['BUILD_PACKAGE']
CODEPIPELINE_NAME = os.environ['CODEPIPELINE_NAME']


def handler(event, context):
    response = []
    try:
        tag_name = str(event['tag_name'])+'.zip' # gets the tag name to be deployed
        logger.info(">> Event: {event}".format(event = str(event)))
        if update_source_package(tag_name): # updates s3 package, will create a new version of the file
            time.sleep(3)
            client = boto3.client('codepipeline') # if succesful.. will start the codepipeline
            logger.info('>> Starting codepipeline execution...')
            response = client.start_pipeline_execution(name=CODEPIPELINE_NAME)
            logger.info('>> Execution succeeded')
            return {
                "statusCode": 200,
                "body": json.dumps('Execution succesful')
            }
        else:
            raise RuntimeError('>> could not update S3 buildpackage')
    except Exception as e:
        logger.info('>> Lambda Handler Error: {Error} '.format(Error = str(e)))
        return {
            "statusCode": 500,
            "body": json.dumps('Erro: {error}'.format(error=str(e)))
        }


def update_source_package(tag_name):
    try:
        client = boto3.client('s3') # will be in charge of updating the S3 bucket build file
        response = client.copy_object(
            Bucket=S3BUCKET,
            CopySource = {'Bucket': S3BUCKET, 'Key': tag_name},
            Key=BUILD_PACKAGE,
            TaggingDirective='REPLACE',
            Tagging="GitHub_Tag={tag_name}".format(tag_name=tag_name)
        )
        logger.info('>> Build package updated using Github Tag: {tag}'.format(tag=tag_name))
        return True # if success returns true
    except Exception as e:
        logger.info('>> Lambda handler Error: {Error}'.format(Error=str(e)))
        return False