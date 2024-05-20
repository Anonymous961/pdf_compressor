import boto3, botocore
import os
from werkzeug.utils import secure_filename
import io
from uuid import uuid4

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
)

def get_files_from_s3():
    bucket_name= os.environ["AWS_BUCKET_NAME"]
    try:
        files = s3.list_objects_v2(Bucket=bucket_name)
        return files, None
    except botocore.exceptions.ClientError as e:
        print("Something went wrong")
        return None, e
def upload_file_to_s3(file_path):
    unique_name=str(uuid4())
    file_extension = os.path.splitext(secure_filename(os.path.basename(file_path)))[1]
    filename= secure_filename(unique_name)+file_extension
    try:
        with open(file_path,"rb") as file:
            s3.upload_fileobj(file, os.environ["AWS_BUCKET_NAME"], filename)
        print("File uploaded successfully")
    except botocore.exceptions.ClientError as e:
        print("Something went wrong uploading file")
        return e
    return filename

def delete_all_objects():
    bucket_name=os.environ['AWS_BUCKET_NAME']

    try:
        response= s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            for obj in response["Contents"]:
                print(f"Deleting {obj['Key']}")
                s3.delete_object(Bucket=bucket_name,Key=obj["Key"])
    except botocore.exceptions.ClientError as e:
        print("Something went wrong uploading file")
        return e
