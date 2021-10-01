import json
import os
import logging
import urllib.parse
import boto3
# from botocore.vendored import requests
import urllib3
http = urllib3.PoolManager()
import re
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SLACK_HOOK = os.environ["SLACK_HOOK"]
client = boto3.client('ecs')

def handler(event, context):
    try:
        if(event["detail-type"] == "Batch Job State Change"):
            print(">> state changed for job")
            if(event["detail"]["status"] == "SUCCEEDED"):
                print(">> task ended....")
                task_arn = event["detail"]["container"]["containerInstanceArn"]
                if("reason" in event["detail"]["container"]):
                    print(event["detail"]["container"]["reason"])
                    post_to_slack("ALARM", "dev", event["detail"]["container"]["reason"], "FF0000", "AWS BATCH", "ALARM", event["detail"]["container"]["reason"], str(task_arn))
                else:
                    post_to_slack("OK", "dev", "Job finished successfully", "#009933", "AWS BATCH", "ALARM", "Job finished successfully", str(task_arn))
                    
        return {"statusCode": 200, "body": json.dumps('ricardo'), "headers": { "headerName": "headerValue"}, "isBase64Encoded": False}
    except Exception as e:
        logger.info("Error >> "+str(e))
        
        
        
def post_to_slack(status_message, envr, message,color_msg, alarm_name, new_state, reason, description):
    try:
        data =  {
                'username': "AWS_BATCH_NOTIFICATIONS",
                'icon_emoji': ":cr7:",
                "attachments": [
                    {
                    "color": color_msg,
                    "blocks": [
                        {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Cloudwatch Alarms in "+str(envr)+" environment"
                            }
                        },
                        {
                        "type": "section",
                        "fields": [
                            {
                            "type": "mrkdwn",
                            "text": "*Environment:*\n"+envr
                            },
                            {
                            "type": "mrkdwn",
                            "text": "*Status:*\n"+new_state
                            },
                            {
                            "type": "mrkdwn",
                            "text": "*Alarm Reason:*\n"+reason
                            },
                            {
                            "type": "mrkdwn",
                            "text": "*Alarm Name*\n"+alarm_name
                            },
                            {
                            "type": "mrkdwn",
                            "text": "*Alarm Description*\n"+description
                            }
                        ]
                        }
                    ]
                    }
                ]
                }
        hooks = [SLACK_HOOK]
        for h in hooks:
            # response = requests.post(h, json.dumps(data), headers={'Content-Type': 'application/json'})
            response = http.request('POST',h, body = json.dumps(data), headers={'Content-Type': 'application/json'}, retries = False)
            print('>> sending to hook '+str(h))
            print(response)
        return 'success'
    except Exception as e:
        print(e)


def get_color(alarm_status):
    try:
        if alarm_status == "ALARM":
            return "FF0000"
        elif alarm_status == "OK":
            return "#009933"
        else:
            return "#0099ff"
    except Exception as e:
        return "FF0000"