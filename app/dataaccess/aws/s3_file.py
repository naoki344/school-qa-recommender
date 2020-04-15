import boto3


class S3FileClient:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')
        self.s3_bucket = self.s3.Bucket(bucket_name)

    def upload_file(self, s3_key: str, data: bytes, content_type: str) -> str:
        self.s3_bucket.put_object(
                Key=s3_key,
                Body=data,
                ContentType=content_type)
        return self.get_obj_url(s3_key)

    def get_obj_url(self, s3_key: str):
        client = boto3.client('s3')
        response = client.get_bucket_location(
                Bucket=self.bucket_name)
        resion = response["LocationConstraint"]
        return f"https://{self.bucket_name}.s3-{resion}.amazonaws.com/{s3_key}"
