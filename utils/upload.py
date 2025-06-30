import os
import uuid
from datetime import datetime
from google.cloud import storage
import boto3
from botocore.exceptions import ClientError
from pymongo.collection import Collection
import db  # MongoDB (optional)

# Set credentials path for Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/credentials.json"

class UploadImage:

    # === Google Cloud Single Upload ===
    @staticmethod
    def upload_to_google_cloud(file, bucket_folder_name: str):
        storage_client = storage.Client()
        bucket_name = 'jagahonline-data'

        try:
            bucket = storage_client.get_bucket(bucket_name)
            extension = file.filename.split('.')[-1]
            new_filename = f"ecom-images/{bucket_folder_name}/{uuid.uuid4()}.{extension}"

            blob = bucket.blob(new_filename)
            blob.content_type = file.content_type
            blob.upload_from_file(file.file)

            return f"https://storage.googleapis.com/{bucket_name}/{new_filename}"
        except Exception as e:
            print(f"[GCS Upload Error]: {e}")
            return None

    # === DigitalOcean Spaces Upload ===
    @staticmethod
    def upload_to_digital_ocean(file, bucket_folder_name: str, log_collection: Collection = None):
        ACCESS_ID = 'YK3ACUR37NIFCZNKGUC5'
        SECRET_KEY = 'wZWiWX2OjFbQoPE7RuNApnaoiukRPqzWumRWfJAaEzI'

        session = boto3.session.Session()
        client = session.client(
            's3',
            region_name='jocdn',
            endpoint_url='https://jocdn.sfo3.digitaloceanspaces.com',
            aws_access_key_id=ACCESS_ID,
            aws_secret_access_key=SECRET_KEY
        )

        extension = file.filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{extension}"
        file_path = f"{bucket_folder_name}/{new_filename}"

        try:
            client.upload_fileobj(
                file.file,
                Bucket='jo-classified',
                Key=file_path,
                ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type}
            )

            # Optional: Save upload record in MongoDB
            if log_collection is not None:
                log_collection.insert_one({
                "file_name": new_filename,
                "bucket_folder_name": bucket_folder_name,
                "file_path": file_path,
                "file_type": file.content_type,
                "file_size": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })

            return f"https://jocdn.sfo3.cdn.digitaloceanspaces.com/jo-classified/{file_path}"
        except Exception as e:
            print(f"[DO Upload Error]: {e}")
            return None

    # === Folder Existence Check in S3/DO (Optional) ===
    @staticmethod
    def folder_exists(bucket_name, path_to_folder):
        try:
            s3 = boto3.client('s3')
            res = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=path_to_folder
            )
            return 'Contents' in res
        except ClientError as e:
            print(f"[S3 Folder Check Error]: {e}")
            return False
