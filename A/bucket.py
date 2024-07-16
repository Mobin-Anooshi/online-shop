import boto3
import boto3.session
from django.conf import settings

class Bucket :
    def __init__(self) -> None:
        session = boto3.session.Session()
        self.conn = session.client(
            service_name = settings.AWS_SERVICE_NAME,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url = settings.AWS_S3_ENDPOINT_URL
            
        )      
        self.conn2 = boto3.resource(
            service_name = settings.AWS_SERVICE_NAME,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url = settings.AWS_S3_ENDPOINT_URL
            
        )      
        

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        # result = self.conn2.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        # for obj in result.objects.all():
        #     return obj
        if result['KeyCount']:
            return result['Contents']
        else:
            return None
        
    def delete_object(self,key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,Key=key)
        return True

    def download_object(self,key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'bw') as f :
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME,key,f)       
    # def upload_object(self,image):
    #     with open(image['filename'],'rb') as f:
    #         self.conn.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME,image['filename'])
            # self.conn.upload_file(file_name=image.filename,bucket=settings.AWS_STORAGE_BUCKET_NAME,object_name=image)      
bucket = Bucket()

