import json
import os
import boto3
import openai
from openai import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

s3 = boto3.client('s3')
bucket_name = os.getenv('BUCKET_NAME') 


def generate(event, context):
    
    try:  
        for record in event['records']:
            body = json.loads(record['body'])
            topic = body['topic']
            
            prompt = f"""
                can you write a blog on this topic {topic}. Youe blog should be in this structure.
                1. Title
                2. introduction
                3. Body content
                4. conclusion
                5. references
                
                Include various required details in the blog. Don't generate out of the topic.                 
            
            """
            
            response = openai.chat.completions.create(
                        model="gpt-4o-mini-2024-07-18",
                        temperature=0.8,
                        messages=[{"role": "system", "content": prompt},]
            )
            
            
            # Extract the blog content
            blog_content = response.choices[0].message.content
            
            # Save the blog content to a text file in S3
            file_name = f"blog_{topic.replace(' ', '_')}.txt"
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=blog_content)


        return {"statusCode": 200, "body": "successfully created the essay on the topic : {topic} "}
    
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
