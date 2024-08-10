import json
import traceback
import boto3
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Initialize AWS SQS client
sqs = boto3.client("sqs", region_name=os.getenv("REGION_NAME"),)

# output s3 bucket 
s3 = boto3.client('s3')
bucket_name = os.getenv("BUCKET_NAME")

# Set your SQS queue URL
QUEUE_URL = os.getenv("QUEUE_URL")


def send_message_to_queue(message):
    try:
        response = sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=message)
    
    except Exception as e:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Failed to insert pending status: {str(e)}\n{stack_trace}")
    

def QueueHandler(messages):
    print("message count : ",len(messages))
    try:
        messages_dict = [message.dict() for message in messages]
        for message in messages_dict:
            message_body = json.dumps(message)
            send_message_to_queue(message_body)
        return {"response": "successfully uploaded the topics"}
    
    except Exception as e:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=400, detail=f"Failed to invock transcripts: {str(e)}\n{stack_trace}")
   
    
def retrieve_results(session_id):
    file_name = f"blog_{session_id}.txt"
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read().decode('utf-8')
        return file_content
    
    except Exception as e:
        stack_trace = traceback.format_exc()
        raise HTTPException(status_code=400, detail=f"Failed to invock transcripts: {str(e)}\n{stack_trace}")