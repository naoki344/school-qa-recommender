import boto3
import mimetypes


class S3FileClient:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')
        self.s3_bucket = self.s3.Bucket(bucket_name)

    def get_obj_url(self, s3_key: str):
        client = boto3.client('s3')
        response = client.get_bucket_location(
                Bucket=self.bucket_name)
        resion = response["LocationConstraint"]
        return f"https://{self.bucket_name}.s3-{resion}.amazonaws.com/{s3_key}"

    def get(self, s3_key: str) -> bytes:
        '''S3からデータを取得する'''
        result = self.s3_bucket.Object(s3_key).get()
        data = result['Body'].read()
        return data

    def get_list(self, prefix: str):
        return self.s3_bucket.objects.filter(Prefix=prefix)

    def copy(self, from_s3_key, to_bucket, to_s3_key):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(to_bucket)
        bucket.Object(to_s3_key).copy({
            'Bucket': self.bucket_name,
            'Key': from_s3_key
        })
