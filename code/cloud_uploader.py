"""
IMPORTANT:
- ENGR Servers are missing according to pylance
    - boto3
    - botocore.exceptions
    - dotenv
- Install them by entering this:
    - pip install boto3
- Make sure to do:
    - Change to where directory where EdgeGaurd code is store ~/EdgeGuard-Hybrid-Intelligence/code
    - python3 -m venv env
    - source env/bin/activate
    - pip install boto3 python-dotenv
"""
## TODO
"""
- A scripit to complie all the code and pre-reqs for the software are installed
"""


import time
import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

class CloudUploader: 
    # Integration Lead Component:
    # Manages the connection between Edge motion detection and AWS S3
    
    # Init boto3 library
    def __init__(self):
        try: 
            self.s3_client = boto3.client(
                's3',
                # Unknown info at the time of working on this
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-TODO')
            )
            self.bucket_name = os.getenv('S3_BUCKET_NAME') # Find double check
        except Exception as e:
            logging.error(f"Failed to initialize AWS Client: {e}")
    
    # Uploads image and returns the S3 URL for the database.
    def upload_frame(self, file_path):
        object_name = os.path.basename(file_path)
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            # URL for DynamoDB/Dashboard tasks
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
            return s3_url
        except ClientError as e:
            logging.error(f"Upload failed: {e}")
            return None