from typing import BinaryIO
from typing import Optional

import boto3


class S3FileClient:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')
        self.s3_bucket = self.s3.Bucket(bucket_name)

    def upload_file(self,
                    s3_key: str,
                    data: bytes,
                    content_type: Optional[str] = None) -> str:
        if content_type is None:
            self.s3_bucket.put_object(Key=s3_key, Body=data)
        else:
            self.s3_bucket.put_object(Key=s3_key,
                                      Body=data,
                                      ContentType=content_type)
        return self.get_obj_url(s3_key)

    def get_obj_url(self, s3_key: str):
        client = boto3.client('s3')
        response = client.get_bucket_location(Bucket=self.bucket_name)
        resion = response["LocationConstraint"]
        return f"https://{self.bucket_name}.s3-{resion}.amazonaws.com/{s3_key}"

    def get(self, s3_key: str) -> bytes:
        '''S3からデータを取得する'''
        result = self.s3_bucket.Object(s3_key).get()
        data = result['Body'].read()
        return data

    def get_list(self, prefix: str):
        return self.s3_bucket.objects.filter(Prefix=prefix)

    def copy(self, from_file, to_bucket, to_file):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(to_bucket)
        bucket.Object(to_file).copy({
            'Bucket': self.s3_bucket_name,
            'Key': from_file
        })

    def get_fp(self, s3_key: str) -> BinaryIO:
        '''S3からデータを取得する'''
        result = self.s3_bucket.Object(s3_key).get()
        return result['Body']
