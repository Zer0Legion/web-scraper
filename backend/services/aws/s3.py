import uuid
import boto3

from objects.requests.aws_service import UploadImageRequest


class AWSService:
    """
    Service for interacting with AWS.
    """

    def __init__(self) -> None:
        self.s3 = boto3.client("s3")


    def upload_file(self, param: UploadImageRequest):
        """
        Upload a file to an S3 bucket.

        Parameters
        ----------
        file_path : str
            path to the file
        bucket : str
            bucket name
        object_name : str
            object name
        """
        object_name=uuid.uuid4().hex
        self.s3.upload_file(param.file_path, param.bucket, object_name)