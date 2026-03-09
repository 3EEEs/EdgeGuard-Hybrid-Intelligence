# cloud_uploader.py
import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

class CloudUploader: 
    def __init__(self):
        try: 
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-west-2') # Updated to us-west-2
            )
            self.bucket_name = os.getenv('S3_BUCKET_NAME')
        except Exception as e:
            logging.error(f"Failed to initialize AWS Client: {e}")
    
    def upload_frame(self, file_path):
        object_name = os.path.basename(file_path)
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            s3_url = f"https://{self.bucket_name}.s3.us-west-2.amazonaws.com/{object_name}"
            return s3_url
        except ClientError as e:
            logging.error(f"Upload failed: {e}")
            return None