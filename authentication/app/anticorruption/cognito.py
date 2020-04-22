from typing import Optional
from typing import Tuple

'''
{
    "version": "1",
    "region": "ap-northeast-1",
    "userPoolId": "ap-northeast-1_1G6B3pml2",
    "userName": "711bb803-6d15-4c5b-a3b4-757d54af1f9b",
    "callerContext": {
        "awsSdkVersion": "aws-sdk-unknown-unknown",
        "clientId": "6mk3tldtr55q0oc0ime00b90k1"
    },
    "triggerSource": "PostConfirmation_ConfirmSignUp",
    "request": {
        "userAttributes": {
            "sub": "711bb803-6d15-4c5b-a3b4-757d54af1f9b",
            "custom:last_name": "miyoshi",
            "cognito:email_alias": "trombone344+17@gmail.com",
            "cognito:user_status": "CONFIRMED",
            "email_verified": "true",
            "custom:last_name_kana": "miyoshi",
            "custom:first_name": "naoki",
            "nickname": "naoki",
            "email": "trombone344+17@gmail.com",
            "custom:first_name_kana": "naoki"
            "custom:avatar_url": "naoki"
        }
    },
    "response": {}
}
'''


class AvatarImageUrl:
    def __init__(self, value: str):
        self.value = value

    def get_s3_location(self) -> Tuple[str, str]:
        s = self.value.split("/")
        s3_bucket_path = s[2]
        s3_bucket_name = s3_bucket_path.split(".")[0]
        s3_key = "/".join(s[3:])
        return s3_bucket_name, s3_key


class PostConfirmationTransfer:
    def __init__(self, data):
        self.data = data

    def get_user_id(self) -> str:
        return self.data["userName"]

    def get_avatar_url(self) -> Optional[str]:
        url = self.data["request"]["userAttributes"].get("custom:avatar_url")
        if url:
            return AvatarImageUrl(
                self.data["request"]["userAttributes"].get(
                    "custom:avatar_url"))
        return None
