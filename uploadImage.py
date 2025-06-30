import os
from google.cloud import storage
# from app.utils import utils
import uuid
import boto3
from botocore.exceptions import ClientError
from pymongo.collection import Collection
from datetime import datetime


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/credentials.json"

class UploadImage():

    def uploadImageToGoogleCloud(files):
        
        uploaded_files = []
        storage_client = storage.Client()
        bucket_name = 'jagahonline-data'
        
        for img in files:
            
            try:
                bucket = storage_client.get_bucket(bucket_name)
                bucket.location = 'US'
                blob = bucket.blob("ecom-banners/"+img.filename)
                blob.content_type = img.content_type
                blob.upload_from_file(img.file)
                uploaded_files.append(img)
            except Exception as e:
                    print(e)
            
        return uploaded_files
    
    def uploadImageToGoogleCloudSingle(file, bucket_folder_name):
        storage_client = storage.Client()
        bucket_name = 'jagahonline-data'
        
        try:
            bucket = storage_client.get_bucket(bucket_name)
            bucket.location = 'US'
            newFileName = 'ecom-images/'+bucket_folder_name+'/'+ str(uuid.uuid1()) + "."+ file.filename.split(".")[-1]
            blob = bucket.blob('ecom-images/'+bucket_folder_name+'/'+file.filename)
            blob.content_type = file.content_type   
            blob.upload_from_file(file.file)

            bucket.rename_blob(blob,new_name=newFileName)
            return newFileName
            
        except Exception as e:
                    print(e)
                    



    def uploadImage_DO(file,bucket_folder_name):
        ACCESS_ID = 'YK3ACUR37NIFCZNKGUC5'
        SECRET_KEY = 'wZWiWX2OjFbQoPE7RuNApnaoiukRPqzWumRWfJAaEzI'
        ACCESS_TOKEN = "dop_v1_9e3a526689f63346a63d0afc51cf1d33de9b214799a02037647e7afa3653f712"

        # Initiate session
        session = boto3.session.Session()
       
        client = session.client('s3',
                                region_name='jocdn',
                                endpoint_url='https://jocdn.sfo3.digitaloceanspaces.com',
                                aws_access_key_id=ACCESS_ID,
                                aws_secret_access_key=SECRET_KEY)
    
        FILE_UPLOAD_PATH =  bucket_folder_name + "/"
       
        newFileName = str(uuid.uuid1()) + "."+ file.filename.split(".")[-1]

        file_path = FILE_UPLOAD_PATH + newFileName

        # Upload a file to your Space
        client.upload_fileobj(file.file,"jo-classified",  FILE_UPLOAD_PATH + newFileName, ExtraArgs={'ACL':'public-read','ContentType': file.content_type})
        print(file_path)

        db.cdn_contents.insert_one({
            "file_name": newFileName,
            "bucket_folder_name": bucket_folder_name,
            "file_path": file_path,
            "file_type": file.content_type,
            "file_size": "",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })

        return file_path

    
    def uploadfile_DO(file,bucket_folder_name, file_extension):
        ACCESS_ID = 'YK3ACUR37NIFCZNKGUC5'
        SECRET_KEY = 'wZWiWX2OjFbQoPE7RuNApnaoiukRPqzWumRWfJAaEzI'
        ACCESS_TOKEN = "dop_v1_9e3a526689f63346a63d0afc51cf1d33de9b214799a02037647e7afa3653f712"

        # Initiate session
        session = boto3.session.Session()
       
        client = session.client('s3',
                                region_name='jocdn',
                                endpoint_url='https://jocdn.sfo3.digitaloceanspaces.com',
                                aws_access_key_id=ACCESS_ID,
                                aws_secret_access_key=SECRET_KEY)
    
        FILE_UPLOAD_PATH =  bucket_folder_name + "/"
       
        newFileName = str(uuid.uuid1()) + "."+ file_extension

        file_path = FILE_UPLOAD_PATH + newFileName

        client.upload_fileobj(file, 'jo-classified', FILE_UPLOAD_PATH + newFileName, ExtraArgs={'ACL': 'public-read', 'ContentType': "text/csv"})

        print(file_path)
        return file_path

    def folder_exists(bucket_name, path_to_folder):
        try:
            s3 = boto3.client('s3')
            res = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=path_to_folder
            )
            return True
        except ClientError as e:
            # Logic to handle errors.
            raise False
        


#Credentials Used:

IMAGE_URL = "https://storage.googleapis.com/jagahonline-data/"
IMAGE_DO_URL = "https://jocdn.sfo3.cdn.digitaloceanspaces.com/jo-classified/"
BRANDS_IMAGE_URL = "brands/"
BANNER_IMAGE_URL = "banners/"
PROPERTY_IMAGE_URL = "property/"
WORKING_ENVIRONMENT = "development"
API_URL = "http://realstateapi.cloudapiserver.com/"